import json
import urllib.request

with open('public/tracks.json', 'r', encoding='utf-8') as f:
    tracks = json.load(f)

test_indices = [0, 10, 25, 50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 499]

for idx in test_indices:
    t = tracks[idx]
    vid = t['youtubeId']
    url = f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={vid}'
    try:
        with urllib.request.urlopen(url, timeout=4) as res:
            data = json.loads(res.read().decode())
            print(f"#{idx+1} {t['title']} -> {data.get('title')} (Status: OK)")
    except Exception as e:
        print(f"#{idx+1} {t['title']} -> Error: {e}")
