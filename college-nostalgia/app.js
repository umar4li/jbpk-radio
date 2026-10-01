// Application State & Configuration
let playlist = [];
let filteredPlaylist = [];
let currentTrackIndex = 0;
let isPlaying = false;
let isMuted = false;
let isShuffled = false;
let currentCategory = 'all';
let ytPlayer = null;
let ytReady = false;
let updateTimer = null;
let watchdogTimer = null;
let isSeeking = false;
let bgMode = 'art'; // 'art' or 'real'

// DOM Elements
const trackTitle = document.getElementById('trackTitle');
const trackArtist = document.getElementById('trackArtist');
const trackCover = document.getElementById('trackCover');
const trackIndexBadge = document.getElementById('trackIndexBadge');
const vinylDisc = document.getElementById('vinylDisc');
const vinylPulse = document.getElementById('vinylPulse');
const playBtn = document.getElementById('playBtn');
const playIcon = document.getElementById('playIcon');
const pauseIcon = document.getElementById('pauseIcon');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const seekTrack = document.getElementById('seekTrack');
const seekProgress = document.getElementById('seekProgress');
const seekThumb = document.getElementById('seekThumb');
const currentTimeEl = document.getElementById('currentTime');
const durationTimeEl = document.getElementById('durationTime');
const muteBtn = document.getElementById('muteBtn');
const volumeIcon = document.getElementById('volumeIcon');
const toastEl = document.getElementById('toast');

// Top Bar Elements
const clockHour = document.getElementById('clockHour');
const clockMinute = document.getElementById('clockMinute');
const clockPeriod = document.getElementById('clockPeriod');
const onlineCount = document.getElementById('onlineCount');
const panToggleBtn = document.getElementById('panToggleBtn');
const bgSwitchBtn = document.getElementById('bgSwitchBtn');
const heroBg = document.getElementById('heroBg');
const playlistBtn = document.getElementById('playlistBtn');

// Drawer Elements
const drawerBackdrop = document.getElementById('drawerBackdrop');
const drawerPanel = document.getElementById('drawerPanel');
const closeDrawerBtn = document.getElementById('closeDrawerBtn');
const playlistSearch = document.getElementById('playlistSearch');
const playlistList = document.getElementById('playlistList');
const shuffleBtn = document.getElementById('shuffleBtn');
const categoryTabs = document.getElementById('categoryTabs');
const playlistHeaderCount = document.getElementById('playlistHeaderCount');

let toastTimeout = null;

// --- TOAST NOTIFICATION ---
function showToast(msg, duration = 2500) {
  if (!toastEl) return;
  toastEl.textContent = msg;
  toastEl.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-2');
  toastEl.classList.add('opacity-100', 'translate-y-0');

  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => {
    toastEl.classList.remove('opacity-100', 'translate-y-0');
    toastEl.classList.add('opacity-0', 'pointer-events-none', 'translate-y-2');
  }, duration);
}

// --- 1. DYNAMIC YOUTUBE IFRAME API LOADER ---
function loadYouTubeAPI() {
  return new Promise((resolve) => {
    if (window.YT && window.YT.Player) {
      resolve(window.YT);
      return;
    }
    const prevReady = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = function() {
      if (typeof prevReady === 'function') prevReady();
      resolve(window.YT);
    };
    const tag = document.createElement('script');
    tag.src = 'https://www.youtube.com/iframe_api';
    document.head.appendChild(tag);
  });
}

// --- 2. INITIALIZATION ---
async function initApp() {
  // Pre-load YouTube API immediately
  loadYouTubeAPI().then((YT) => {
    initYouTubePlayer(YT);
  }).catch(err => {
    console.warn("YouTube API init error:", err);
  });

  // Fetch Tracks Database
  try {
    const res = await fetch('public/tracks.json?v=' + Date.now());
    if (res.ok) {
      playlist = await res.json();
    } else {
      setTimeout(initApp, 1000);
      return;
    }
  } catch (e) {
    setTimeout(initApp, 1500);
    return;
  }

  // Ensure first song is Aye Meri College Ki Ladkiyon
  if (playlist.length > 0 && !playlist[0].title.toLowerCase().includes("college ki ladkiyon")) {
    const idx = playlist.findIndex(t => t.title.toLowerCase().includes("college ki ladkiyon"));
    if (idx !== -1) {
      const first = playlist.splice(idx, 1)[0];
      playlist.unshift(first);
    }
  }

  filteredPlaylist = [...playlist];
  playlistHeaderCount.textContent = `${playlist.length} Tracks`;

  renderPlaylistDrawer(filteredPlaylist);
  loadTrack(0, false);
  startClock();
  startOnlineCounter();
  setupEventListeners();
  setupSeeking();
}

// --- 3. YOUTUBE PLAYER INITIALIZATION ---
function initYouTubePlayer(YT) {
  const initialId = playlist[0] ? playlist[0].youtubeId : 'hGMvxhd-Z0s';
  ytPlayer = new YT.Player('ytPlayer', {
    height: '180',
    width: '320',
    videoId: initialId,
    playerVars: {
      controls: 0,
      disablekb: 1,
      playsinline: 1,
      rel: 0,
      modestbranding: 1,
      autoplay: 0,
      iv_load_policy: 3,
      origin: window.location.origin
    },
    events: {
      onReady: () => {
        ytReady = true;
        console.log("YouTube Player Ready!");
        if (isPlaying) {
          playCurrent();
        }
      },
      onStateChange: (event) => {
        if (event.data === YT.PlayerState.PLAYING) {
          clearWatchdog();
          const track = playlist[currentTrackIndex];
          trackTitle.textContent = track.title; // clear loading badge
          setPlayingUI(true);
        } else if (event.data === YT.PlayerState.PAUSED) {
          setPlayingUI(false);
        } else if (event.data === YT.PlayerState.ENDED) {
          playNext();
        } else if (event.data === YT.PlayerState.BUFFERING) {
          if (isPlaying) {
            vinylDisc.style.animationPlayState = 'running';
          }
        }
      },
      onError: (err) => {
        console.warn("YouTube Player error:", err);
        clearWatchdog();
        showToast("⚠️ Song restricted by publisher, playing next hit...", 2000);
        setTimeout(playNext, 1000);
      }
    }
  });
}

function clearWatchdog() {
  if (watchdogTimer) {
    clearTimeout(watchdogTimer);
    watchdogTimer = null;
  }
}

// --- 4. TRACK LOADING & RESILIENT PLAYBACK ---
function loadTrack(index, autoPlay = true) {
  clearWatchdog();

  if (index < 0) index = playlist.length - 1;
  if (index >= playlist.length) index = 0;
  
  currentTrackIndex = index;
  const track = playlist[currentTrackIndex];

  // Update UI Elements
  if (autoPlay) {
    trackTitle.innerHTML = `${track.title} <span class="text-xs text-amber-300 font-normal animate-pulse">(Connecting...)</span>`;
  } else {
    trackTitle.textContent = track.title;
  }
  trackArtist.textContent = `${track.artist} • ${track.album}`;
  trackCover.src = track.cover || `https://img.youtube.com/vi/${track.youtubeId}/hqdefault.jpg`;
  
  if (track.isJbSpecial) {
    trackIndexBadge.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>JB MIX`;
  } else {
    trackIndexBadge.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>LIVE`;
  }

  // Reset Progress Bar
  seekProgress.style.width = '0%';
  seekThumb.style.left = '0%';
  currentTimeEl.textContent = '0:00';
  durationTimeEl.textContent = '0:00';

  updateDrawerActiveTrack();

  if (ytPlayer && ytReady) {
    try {
      if (autoPlay) {
        ytPlayer.loadVideoById({
          videoId: track.youtubeId,
          startSeconds: 0
        });
        if (typeof ytPlayer.unMute === 'function' && !isMuted) {
          ytPlayer.unMute();
          ytPlayer.setVolume(100);
        }
        if (typeof ytPlayer.playVideo === 'function') {
          ytPlayer.playVideo();
        }
        setPlayingUI(true);

        // 4.5-second Watchdog Timer: if video stalls or fails to play
        watchdogTimer = setTimeout(() => {
          if (ytPlayer && typeof ytPlayer.getPlayerState === 'function') {
            const state = ytPlayer.getPlayerState();
            if (state !== 1) { // Not playing
              console.warn("Watchdog: Song stalled, attempting retry or next song...");
              try { ytPlayer.playVideo(); } catch(e){}
              setTimeout(() => {
                if (ytPlayer.getPlayerState() !== 1) {
                  showToast("⚠️ Video slow or blocked, playing next...", 1800);
                  playNext();
                }
              }, 2000);
            }
          }
        }, 4500);

      } else {
        ytPlayer.cueVideoById(track.youtubeId);
      }
    } catch (e) {
      console.warn("YouTube load error:", e);
    }
  }

  if (autoPlay) {
    isPlaying = true;
    setPlayingUI(true);
  }
}

function playCurrent() {
  isPlaying = true;
  const track = playlist[currentTrackIndex];
  
  if (ytPlayer && ytReady) {
    try {
      const state = ytPlayer.getPlayerState ? ytPlayer.getPlayerState() : -1;
      if (state === -1 || state === 5 || state === 0) {
        ytPlayer.loadVideoById({
          videoId: track.youtubeId,
          startSeconds: 0
        });
      }
      if (typeof ytPlayer.unMute === 'function' && !isMuted) {
        ytPlayer.unMute();
        ytPlayer.setVolume(100);
      }
      ytPlayer.playVideo();
      setPlayingUI(true);
    } catch (e) {
      console.warn("playCurrent error:", e);
    }
  } else {
    setPlayingUI(true);
    setTimeout(() => {
      if (ytPlayer && ytReady) {
        playCurrent();
      }
    }, 400);
  }
}

function pauseCurrent() {
  isPlaying = false;
  clearWatchdog();
  if (ytPlayer && ytReady) {
    try {
      ytPlayer.pauseVideo();
    } catch (e) {}
  }
  setPlayingUI(false);
}

function togglePlay() {
  if (isPlaying) {
    pauseCurrent();
  } else {
    playCurrent();
  }
}

function playNext() {
  if (isShuffled) {
    const nextIdx = Math.floor(Math.random() * playlist.length);
    loadTrack(nextIdx, true);
  } else {
    loadTrack(currentTrackIndex + 1, true);
  }
}

function playPrev() {
  if (ytPlayer && ytReady) {
    try {
      const pos = ytPlayer.getCurrentTime();
      if (pos > 4) {
        ytPlayer.seekTo(0, true);
        return;
      }
    } catch (e) {}
  }
  loadTrack(currentTrackIndex - 1, true);
}

function setPlayingUI(playing) {
  isPlaying = playing;
  playBtn.setAttribute('aria-pressed', playing ? 'true' : 'false');

  if (playing) {
    playIcon.classList.add('hidden');
    pauseIcon.classList.remove('hidden');
    vinylDisc.style.animationPlayState = 'running';
    vinylPulse.style.opacity = '0.5';
    startProgressPolling();
  } else {
    playIcon.classList.remove('hidden');
    pauseIcon.classList.add('hidden');
    vinylDisc.style.animationPlayState = 'paused';
    vinylPulse.style.opacity = '0';
    stopProgressPolling();
  }
  updateDrawerActiveTrack();
}

// --- 5. PROGRESS BAR & FULL-LENGTH TIME POLLING ---
function formatTime(seconds) {
  if (isNaN(seconds) || seconds < 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, '0')}`;
}

function updateProgress() {
  if (isSeeking || !ytPlayer || !ytReady) return;

  try {
    const current = ytPlayer.getCurrentTime() || 0;
    const duration = ytPlayer.getDuration() || 0;

    if (duration > 0) {
      const fraction = Math.min(1, Math.max(0, current / duration));
      const percent = (fraction * 100).toFixed(2);
      seekProgress.style.width = `${percent}%`;
      seekThumb.style.left = `${percent}%`;
      currentTimeEl.textContent = formatTime(current);
      durationTimeEl.textContent = formatTime(duration);
    }
  } catch (e) {}
}

function startProgressPolling() {
  stopProgressPolling();
  updateTimer = setInterval(updateProgress, 300);
}

function stopProgressPolling() {
  if (updateTimer) {
    clearInterval(updateTimer);
    updateTimer = null;
  }
}

function seekToFraction(fraction) {
  fraction = Math.max(0, Math.min(1, fraction));
  const percent = (fraction * 100).toFixed(2);
  seekProgress.style.width = `${percent}%`;
  seekThumb.style.left = `${percent}%`;

  if (ytPlayer && ytReady) {
    try {
      const d = ytPlayer.getDuration();
      if (d && d > 0) {
        ytPlayer.seekTo(d * fraction, true);
        currentTimeEl.textContent = formatTime(d * fraction);
      }
    } catch (e) {}
  }
}

function setupSeeking() {
  function handleSeek(e) {
    const rect = seekTrack.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const fraction = x / rect.width;
    seekToFraction(fraction);
  }

  seekTrack.addEventListener('click', handleSeek);

  seekTrack.addEventListener('mousedown', (e) => {
    isSeeking = true;
    handleSeek(e);

    function onMouseMove(moveEvent) {
      const rect = seekTrack.getBoundingClientRect();
      const x = moveEvent.clientX - rect.left;
      const fraction = Math.max(0, Math.min(1, x / rect.width));
      seekProgress.style.width = `${fraction * 100}%`;
      seekThumb.style.left = `${fraction * 100}%`;
    }

    function onMouseUp(upEvent) {
      isSeeking = false;
      const rect = seekTrack.getBoundingClientRect();
      const x = upEvent.clientX - rect.left;
      seekToFraction(x / rect.width);
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    }

    document.addEventListener('mousemove', onMouseMove);
    document.addEventListener('mouseup', onMouseUp);
  });
}

// --- 6. TOP STATUS BAR (Clock & Live Online Counter) ---
function startClock() {
  const formatter = new Intl.DateTimeFormat('en-IN', {
    timeZone: 'Asia/Kolkata',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  });

  function update() {
    const parts = formatter.formatToParts(new Date());
    const h = parts.find(p => p.type === 'hour')?.value || '12';
    const m = parts.find(p => p.type === 'minute')?.value || '00';
    const p = parts.find(p => p.type === 'dayPeriod')?.value || 'PM';

    clockHour.textContent = h;
    clockMinute.textContent = m;
    clockPeriod.textContent = p;
  }

  update();
  setInterval(update, 1000);
}

function startOnlineCounter() {
  let count = 38;

  function jitter() {
    const delta = Math.random() < 0.5 ? 1 : -1;
    const step = 1 + Math.floor(Math.random() * 3);
    count = Math.max(18, Math.min(64, count + delta * step));
    onlineCount.textContent = count;

    setTimeout(jitter, 3000 + Math.random() * 3500);
  }

  setTimeout(jitter, 3000);
}

// --- 7. 500-SONG PLAYLIST DRAWER & CATEGORY FILTERING ---
function renderPlaylistDrawer(tracks) {
  playlistList.innerHTML = '';
  const fragment = document.createDocumentFragment();

  // Render top 120 items first for instant responsiveness
  const renderSlice = tracks.slice(0, 120);

  renderSlice.forEach((track) => {
    const originalIndex = playlist.indexOf(track);
    const isCurrent = originalIndex === currentTrackIndex;

    const row = document.createElement('div');
    row.className = `flex items-center gap-3 p-2 rounded-xl cursor-pointer transition ${
      isCurrent ? 'bg-white/20 border border-white/25 text-white' : 'hover:bg-white/10 text-white/80'
    }`;
    row.dataset.index = originalIndex;

    row.innerHTML = `
      <div class="relative h-10 w-10 shrink-0 rounded-lg overflow-hidden bg-black/40 border border-white/10">
        <img src="${track.cover || `https://img.youtube.com/vi/${track.youtubeId}/hqdefault.jpg`}" 
             alt="${track.title}" class="h-full w-full object-cover" loading="lazy" />
        ${isCurrent && isPlaying ? `
          <div class="absolute inset-0 bg-black/50 flex items-center justify-center gap-0.5">
            <span class="w-1 bg-green-400 rounded-full eq-bar-1"></span>
            <span class="w-1 bg-green-400 rounded-full eq-bar-2"></span>
            <span class="w-1 bg-green-400 rounded-full eq-bar-3"></span>
          </div>
        ` : ''}
      </div>

      <div class="min-w-0 flex-1">
        <p class="truncate text-sm font-semibold ${isCurrent ? 'text-white' : 'text-white/90'}">${track.title}</p>
        <p class="truncate text-xs text-white/60">${track.artist} • ${track.album}</p>
      </div>

      <div class="text-white/40 shrink-0 pr-1 flex items-center">
        ${isCurrent ? `
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
        ` : `
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" opacity="0.4">
            <path d="M8 5v14l11-7z"/>
          </svg>
        `}
      </div>
    `;

    row.addEventListener('click', () => {
      loadTrack(originalIndex, true);
      closeDrawer();
    });

    fragment.appendChild(row);
  });

  playlistList.appendChild(fragment);

  // Lazy load remaining tracks on scroll
  if (tracks.length > 120) {
    let loadedCount = 120;
    const onScroll = () => {
      if (playlistList.scrollTop + playlistList.clientHeight >= playlistList.scrollHeight - 100) {
        const nextSlice = tracks.slice(loadedCount, loadedCount + 100);
        const subFrag = document.createDocumentFragment();
        nextSlice.forEach((track) => {
          const originalIndex = playlist.indexOf(track);
          const isCurrent = originalIndex === currentTrackIndex;
          const row = document.createElement('div');
          row.className = `flex items-center gap-3 p-2 rounded-xl cursor-pointer transition ${
            isCurrent ? 'bg-white/20 border border-white/25 text-white' : 'hover:bg-white/10 text-white/80'
          }`;
          row.dataset.index = originalIndex;
          row.innerHTML = `
            <div class="relative h-10 w-10 shrink-0 rounded-lg overflow-hidden bg-black/40 border border-white/10">
              <img src="${track.cover || `https://img.youtube.com/vi/${track.youtubeId}/hqdefault.jpg`}" 
                   alt="${track.title}" class="h-full w-full object-cover" loading="lazy" />
            </div>
            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-semibold ${isCurrent ? 'text-white' : 'text-white/90'}">${track.title}</p>
              <p class="truncate text-xs text-white/60">${track.artist} • ${track.album}</p>
            </div>
            <div class="text-white/40 shrink-0 pr-1 flex items-center">
              ${isCurrent ? `
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
              ` : `
                <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor" opacity="0.4">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              `}
            </div>
          `;
          row.addEventListener('click', () => {
            loadTrack(originalIndex, true);
            closeDrawer();
          });
          subFrag.appendChild(row);
        });
        playlistList.appendChild(subFrag);
        loadedCount += 100;
        if (loadedCount >= tracks.length) {
          playlistList.removeEventListener('scroll', onScroll);
        }
      }
    };
    playlistList.addEventListener('scroll', onScroll);
  }
}

function updateDrawerActiveTrack() {
  if (playlistList.children.length === 0) return;
  const items = playlistList.children;
  for (let item of items) {
    const idx = parseInt(item.dataset.index, 10);
    if (idx === currentTrackIndex) {
      item.classList.add('bg-white/20', 'border', 'border-white/25');
      item.classList.remove('hover:bg-white/10');
    } else {
      item.classList.remove('bg-white/20', 'border', 'border-white/25');
      item.classList.add('hover:bg-white/10');
    }
  }
}

function openDrawer() {
  drawerBackdrop.classList.add('open');
  drawerPanel.classList.add('open');
  playlistSearch.value = '';
  applyFilters();
}

function closeDrawer() {
  drawerBackdrop.classList.remove('open');
  drawerPanel.classList.remove('open');
}

function applyFilters() {
  const query = playlistSearch.value.toLowerCase().trim();
  filteredPlaylist = playlist.filter(track => {
    let matchesCategory = false;
    if (currentCategory === 'all') {
      matchesCategory = true;
    } else if (currentCategory === 'jb_special') {
      matchesCategory = track.isJbSpecial === true;
    } else {
      matchesCategory = track.category === currentCategory;
    }
    const matchesSearch = !query || 
      track.title.toLowerCase().includes(query) ||
      track.artist.toLowerCase().includes(query) ||
      track.album.toLowerCase().includes(query);
    return matchesCategory && matchesSearch;
  });

  if (currentCategory === 'jb_special') {
    playlistHeaderCount.textContent = 'JB Special Mix';
  } else if (currentCategory === 'slowed') {
    playlistHeaderCount.textContent = 'Slowed & Lofi';
  } else if (currentCategory === 'romantic') {
    playlistHeaderCount.textContent = 'Romantic Hits';
  } else if (currentCategory === 'classic') {
    playlistHeaderCount.textContent = 'Veer-Zaara & Classics';
  } else {
    playlistHeaderCount.textContent = 'Live Radio';
  }
  renderPlaylistDrawer(filteredPlaylist);
}

// --- 8. EVENT LISTENERS, CONTROLS & SHORTCUTS ---
function setupEventListeners() {
  playBtn.addEventListener('click', togglePlay);
  prevBtn.addEventListener('click', playPrev);
  nextBtn.addEventListener('click', playNext);

  // Mute / Unmute
  muteBtn.addEventListener('click', () => {
    isMuted = !isMuted;
    if (ytPlayer && ytReady) {
      if (isMuted) ytPlayer.mute();
      else ytPlayer.unMute();
    }
    volumeIcon.style.opacity = isMuted ? '0.3' : '1';
    showToast(isMuted ? "🔇 Audio Muted" : "🔊 Audio Unmuted", 1500);
  });

  // Shuffle Toggle
  shuffleBtn.addEventListener('click', () => {
    isShuffled = !isShuffled;
    shuffleBtn.classList.toggle('bg-white', isShuffled);
    shuffleBtn.classList.toggle('text-black', isShuffled);
    shuffleBtn.classList.toggle('bg-white/10', !isShuffled);
    shuffleBtn.classList.toggle('text-white', !isShuffled);
    showToast(isShuffled ? "🔀 Shuffle Mode: ON" : "➡️ Shuffle Mode: OFF", 1500);
  });

  // Background Mode Toggle (Art Illustration vs Real Photo)
  bgSwitchBtn.addEventListener('click', () => {
    if (bgMode === 'art') {
      bgMode = 'real';
      heroBg.style.backgroundImage = "url('public/college-bg-real.png')";
      showToast("🖼️ Background: Real Campus Photo", 1500);
    } else {
      bgMode = 'art';
      heroBg.style.backgroundImage = "url('public/college-bg.png')";
      showToast("🎨 Background: Anime Illustration", 1500);
    }
  });

  // Panorama Pan Mode Toggle
  panToggleBtn.addEventListener('click', () => {
    heroBg.classList.toggle('pan-mode');
    const isPanning = heroBg.classList.contains('pan-mode');
    panToggleBtn.classList.toggle('bg-white/25', isPanning);
    showToast(isPanning ? "🌐 Panorama Motion: ON" : "⏸️ Panorama Motion: OFF", 1500);
  });

  // Drawer Controls
  playlistBtn.addEventListener('click', openDrawer);
  closeDrawerBtn.addEventListener('click', closeDrawer);
  drawerBackdrop.addEventListener('click', closeDrawer);

  // Category Tabs Click
  categoryTabs.addEventListener('click', (e) => {
    const btn = e.target.closest('.cat-tab');
    if (!btn) return;
    document.querySelectorAll('.cat-tab').forEach(b => {
      b.classList.remove('bg-white', 'text-black', 'font-semibold');
      b.classList.add('bg-white/10', 'text-white/80');
    });
    btn.classList.add('bg-white', 'text-black', 'font-semibold');
    btn.classList.remove('bg-white/10', 'text-white/80');

    currentCategory = btn.dataset.cat;
    applyFilters();
  });

  // Search Filter
  playlistSearch.addEventListener('input', applyFilters);



  // Attendance Pls Modal Controls
  const attendanceBtn = document.getElementById('attendanceBtn');
  const attendanceModal = document.getElementById('attendanceModal');
  const attendanceModalBackdrop = document.getElementById('attendanceModalBackdrop');
  const closeAttendanceBtn = document.getElementById('closeAttendanceBtn');

  function openAttendanceModal() {
    if (!attendanceModal || !attendanceModalBackdrop) return;
    attendanceModalBackdrop.classList.remove('opacity-0', 'pointer-events-none');
    attendanceModalBackdrop.classList.add('opacity-100', 'pointer-events-auto');
    attendanceModal.classList.remove('opacity-0', 'pointer-events-none', 'scale-95');
    attendanceModal.classList.add('opacity-100', 'pointer-events-auto', 'scale-100');
    showToast("✋ Thanks! Attendance Marked (pom pom!)", 2000);
  }

  function closeAttendanceModal() {
    if (!attendanceModal || !attendanceModalBackdrop) return;
    attendanceModalBackdrop.classList.remove('opacity-100', 'pointer-events-auto');
    attendanceModalBackdrop.classList.add('opacity-0', 'pointer-events-none');
    attendanceModal.classList.remove('opacity-100', 'pointer-events-auto', 'scale-100');
    attendanceModal.classList.add('opacity-0', 'pointer-events-none', 'scale-95');
  }

  if (attendanceBtn) attendanceBtn.addEventListener('click', openAttendanceModal);
  if (closeAttendanceBtn) closeAttendanceBtn.addEventListener('click', closeAttendanceModal);
  if (attendanceModalBackdrop) attendanceModalBackdrop.addEventListener('click', closeAttendanceModal);

  // 30-Second Timer to Reveal Instagram Widget
  setTimeout(() => {
    const insta = document.getElementById('instaWidget');
    if (insta) {
      insta.classList.remove('opacity-0', 'pointer-events-none', 'translate-y-4');
      insta.classList.add('opacity-100', 'pointer-events-auto', 'translate-y-0');
      showToast("📸 Instagram link active!", 2000);
    }
  }, 30000);

  // Global Keyboard Shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT') return;

    if (e.code === 'Space') {
      e.preventDefault();
      togglePlay();
    } else if (e.code === 'ArrowRight') {
      e.preventDefault();
      playNext();
    } else if (e.code === 'ArrowLeft') {
      e.preventDefault();
      playPrev();
    } else if (e.key === 'm' || e.key === 'M') {
      muteBtn.click();
    } else if (e.key === 'p' || e.key === 'P') {
      if (drawerPanel.classList.contains('open')) closeDrawer();
      else openDrawer();
    } else if (e.key === 's' || e.key === 'S') {
      shuffleBtn.click();
    } else if (e.key === 'Escape') {
      closeDrawer();
      closeAttendanceModal();
    }
  });
}

// Start app
document.addEventListener('DOMContentLoaded', initApp);
