import sys
import json
import re
import urllib.request

def add_song(url_or_id, category="romantic"):
    # Extract YouTube ID
    match = re.search(r'(?:v=|\/|youtu\.be\/)([a-zA-Z0-9_-]{11})', url_or_id)
    if not match:
        print("❌ Invalid YouTube URL or Video ID!")
        return
    vid = match.group(1)

    print(f"🔍 Fetching details for: {vid} ...")
    try:
        api_url = f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={vid}'
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=6) as res:
            info = json.loads(res.read())
            raw_title = info.get('title', 'New Track')
            artist = info.get('author_name', 'Various Artists')
    except Exception as e:
        print(f"⚠️ Could not fetch auto-title ({e}), using default...")
        raw_title = "New Song"
        artist = "Various Artists"

    # Clean title
    title = re.sub(r'\(Official.*?\)|\[Official.*?\]|\|.*', '', raw_title).strip() or raw_title

    # Load existing tracks
    with open('public/tracks.json', 'r', encoding='utf-8') as f:
        tracks = json.load(f)

    # Check duplicate
    for t in tracks:
        if t.get('youtubeId') == vid:
            print(f"⚠️ This song is already in your playlist: {t.get('title')}")
            return

    new_entry = {
        "id": vid,
        "youtubeId": vid,
        "title": title,
        "artist": artist,
        "album": "JB Campus Radio",
        "category": category,
        "isJbSpecial": (category == "jb_special"),
        "cover": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
    }

    # Insert after Track 1
    tracks.insert(1, new_entry)

    with open('public/tracks.json', 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=2)

    print(f"✅ Success! Added '{title}' by '{artist}' to [{category}] category!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_song.py <YouTube_URL_or_ID> [category]")
        print("Categories: jb_special, slowed, romantic, classic, college, masti, sad")
    else:
        url = sys.argv[1]
        cat = sys.argv[2] if len(sys.argv) > 2 else "jb_special"
        add_song(url, cat)
