import json
import urllib.request
import urllib.parse
import re
from concurrent.futures import ThreadPoolExecutor

with open('public/tracks.json', 'r', encoding='utf-8') as f:
    tracks = json.load(f)

def check_track(item):
    idx, t = item
    vid = t.get('youtubeId', '')
    if not vid:
        return idx, t, True
    url = f'https://www.youtube.com/embed/{vid}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=3.5) as res:
            html = res.read().decode('utf-8', errors='ignore')
            unplayable = 'UNPLAYABLE' in html or 'Playback on other websites has been disabled' in html
            return idx, t, unplayable
    except Exception as e:
        return idx, t, True

print("Scanning all 500 tracks...")
indexed_tracks = list(enumerate(tracks))
with ThreadPoolExecutor(max_workers=25) as executor:
    results = list(executor.map(check_track, indexed_tracks))

unplayable_list = [r for r in results if r[2]]
print(f"Total unplayable tracks found: {len(unplayable_list)} out of {len(tracks)}")
for idx, t, _ in unplayable_list[:25]:
    print(f"#{idx+1}: {t['title']} (vid: {t['youtubeId']})")

with open('unplayable.json', 'w', encoding='utf-8') as f:
    json.dump([{'idx': r[0], 'title': r[1]['title'], 'artist': r[1]['artist'], 'album': r[1]['album'], 'vid': r[1]['youtubeId']} for r in unplayable_list], f, indent=2)
