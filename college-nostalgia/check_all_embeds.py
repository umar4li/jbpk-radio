import json
import urllib.request
import sys
from concurrent.futures import ThreadPoolExecutor

with open('public/tracks.json', 'r', encoding='utf-8') as f:
    tracks = json.load(f)

print(f"Checking {len(tracks)} tracks for embed availability...")

def test_embed(item):
    idx, t = item
    vid = t.get('youtubeId')
    url = f'https://www.youtube.com/embed/{vid}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=4) as res:
            body = res.read().decode('utf-8', errors='ignore')
            unplayable = ('UNPLAYABLE' in body or 
                          'Playback on other websites has been disabled' in body or
                          'Video unavailable' in body)
            return idx, t, unplayable
    except Exception as e:
        return idx, t, True

indexed = list(enumerate(tracks))
with ThreadPoolExecutor(max_workers=30) as executor:
    results = list(executor.map(test_embed, indexed))

unplayable = [r for r in results if r[2]]
print(f"Total unplayable found: {len(unplayable)}")

with open('unplayable_ids.json', 'w', encoding='utf-8') as out_f:
    json.dump([{'idx': r[0], 'title': r[1]['title'], 'artist': r[1]['artist'], 'vid': r[1]['youtubeId']} for r in unplayable], out_f, indent=2)

print("Saved unplayable_ids.json")
