import urllib.request
import json
import re

playlist_url = 'https://www.youtube.com/playlist?list=PL-4vYzWm1VTRt8cjl5B9XVnnAsGtTHoKf'
req = urllib.request.Request(playlist_url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

with urllib.request.urlopen(req, timeout=10) as res:
    html = res.read().decode('utf-8', errors='ignore')

# find all videoId in html with titles
matches = re.findall(r'\"videoId\":\"([a-zA-Z0-9_-]{11})\",\"thumbnail\":.*?\"title\":\{\"runs\":\[\{\"text\":\"(.*?)\"\}\]', html)
print(f"Matches count: {len(matches)}")
seen = set()
unique_matches = []
for vid, title in matches:
    if vid not in seen:
        seen.add(vid)
        unique_matches.append((vid, title))

print(f"Unique videos: {len(unique_matches)}")
for idx, (vid, title) in enumerate(unique_matches[:25]):
    print(f"{idx+1}. {vid} : {title}")
