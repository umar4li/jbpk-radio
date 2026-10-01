import urllib.request
import re
import json

# Fetching all videoIds and titles from the user's links
urls = [
    ("track8", "College Nostalgia", "https://youtu.be/iEpHUkH61rU"),
    ("mix1", "Slowed & Lofi", "https://www.youtube.com/watch?v=EBoV6-MrvNs&list=RDEBoV6-MrvNs"),
    ("mix2", "Romantic Melodies", "https://www.youtube.com/watch?v=RNXYQ-LViAI&list=RDRNXYQ-LViAI"),
    ("mix3", "Slowed & Lofi", "https://www.youtube.com/watch?v=qsNAD6gFIEk&list=RDGMEMCMFH2exzjBeE_zAHHJOdxg"),
    ("mix4", "Slowed & Lofi", "https://www.youtube.com/watch?v=ceqt8IlnYUg&list=RDceqt8IlnYUg"),
    ("mix5", "Romantic Melodies", "https://www.youtube.com/watch?v=cn84fZBjgnI&list=RDcn84fZBjgnI"),
    ("track6", "JB Top Radio", "https://youtu.be/SQ4jZ-EAL88"),
    ("playlist7", "Veer-Zaara & Bollywood Classics", "https://www.youtube.com/watch?v=m6Y8xEfyXTs&list=PL-4vYzWm1VTRt8cjl5B9XVnnAsGtTHoKf")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def extract_items(url, default_cat):
    items = []
    # If direct video
    if 'youtu.be/' in url and '&list=' not in url:
        vid = url.split('/')[-1].split('?')[0]
        # Get title via noembed
        try:
            req = urllib.request.Request(f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={vid}', headers=headers)
            with urllib.request.urlopen(req, timeout=5) as res:
                data = json.loads(res.read())
                title = data.get('title', 'Unknown')
                artist = data.get('author_name', 'Various Artists')
                items.append({'youtubeId': vid, 'title': title, 'artist': artist, 'category': default_cat})
        except Exception as e:
            items.append({'youtubeId': vid, 'title': 'Music Track', 'artist': 'Various Artists', 'category': default_cat})
        return items

    # If mix / playlist
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as res:
            html = res.read().decode('utf-8', errors='ignore')
        
        # Traverse ytInitialData
        m = re.search(r'var ytInitialData = ({.*?});</script>', html)
        if not m:
            m = re.search(r'ytInitialData\s*=\s*({.+?});', html)
        if m:
            data = json.loads(m.group(1))
            def walk(d):
                if isinstance(d, dict):
                    if 'playlistPanelVideoRenderer' in d:
                        r = d['playlistPanelVideoRenderer']
                        vid = r.get('videoId')
                        title = r.get('title', {}).get('simpleText') or (r.get('title', {}).get('runs', [{}])[0].get('text', ''))
                        byline = r.get('longBylineText', {}).get('runs', [{}])[0].get('text', '') or r.get('shortBylineText', {}).get('runs', [{}])[0].get('text', '')
                        if vid and title:
                            items.append({'youtubeId': vid, 'title': title, 'artist': byline, 'category': default_cat})
                    elif 'playlistVideoRenderer' in d:
                        r = d['playlistVideoRenderer']
                        vid = r.get('videoId')
                        title = r.get('title', {}).get('runs', [{}])[0].get('text', '') or r.get('title', {}).get('simpleText', '')
                        byline = r.get('shortBylineText', {}).get('runs', [{}])[0].get('text', '')
                        if vid and title:
                            items.append({'youtubeId': vid, 'title': title, 'artist': byline, 'category': default_cat})
                    for v in d.values():
                        walk(v)
                elif isinstance(d, list):
                    for x in d:
                        walk(x)
            walk(data)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return items

new_tracks = []
seen_ids = set()

# Clean title helper
def clean_title(title):
    t = re.sub(r'\(Official Video.*?\)', '', title, flags=re.IGNORECASE)
    t = re.sub(r'\[Official Video.*?\]', '', t, flags=re.IGNORECASE)
    t = re.sub(r'\|.*?(Full Song|YRF|T-Series|Tips|Zee Music).*', '', t, flags=re.IGNORECASE)
    t = re.sub(r'#.*', '', t)
    t = re.sub(r'\s+', ' ', t).strip(' |-_')
    return t or title

# 1. First track MUST BE Link 8: iEpHUkH61rU
track8_item = {
    "id": "iEpHUkH61rU",
    "youtubeId": "iEpHUkH61rU",
    "title": "Aye Meri Natkhati College Ki Ladkiyon",
    "artist": "Udit Narayan",
    "album": "Yeh Dil Aashiqana (2002)",
    "year": "2002",
    "category": "College Nostalgia",
    "duration": 348,
    "cover": "https://img.youtube.com/vi/iEpHUkH61rU/hqdefault.jpg"
}
new_tracks.append(track8_item)
seen_ids.add("iEpHUkH61rU")

# 2. Extract all from user links
print("Fetching tracks from user links...")
for key, cat, u in urls:
    if key == "track8":
        continue
    items = extract_items(u, cat)
    print(f"Extracted from {key} ({cat}): {len(items)} items")
    for it in items:
        vid = it['youtubeId']
        if vid and vid not in seen_ids:
            seen_ids.add(vid)
            clean_t = clean_title(it['title'])
            clean_a = it['artist'] or "Bollywood Artist"
            new_tracks.append({
                "id": vid,
                "youtubeId": vid,
                "title": clean_t,
                "artist": clean_a,
                "album": "JB Campus Radio",
                "year": "2024",
                "category": it['category'],
                "duration": 280,
                "cover": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
            })

print(f"Total new tracks from user links: {len(new_tracks)}")

# 3. Load existing tracks from public/tracks.json to merge and retain vast catalog
with open('public/tracks.json', 'r', encoding='utf-8') as f:
    existing_tracks = json.load(f)

for et in existing_tracks:
    vid = et.get('youtubeId')
    if vid and vid not in seen_ids:
        seen_ids.add(vid)
        new_tracks.append(et)

print(f"Combined total tracks in playlist: {len(new_tracks)}")

# Save updated tracks.json
with open('public/tracks.json', 'w', encoding='utf-8') as f:
    json.dump(new_tracks, f, ensure_ascii=False, indent=2)

print("Saved combined tracks to public/tracks.json successfully!")
