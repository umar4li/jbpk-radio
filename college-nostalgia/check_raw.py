import re

with open('fetch_playlist7.py', 'r') as f:
    pass

import urllib.request

url = 'https://www.youtube.com/playlist?list=PL-4vYzWm1VTRt8cjl5B9XVnnAsGtTHoKf'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    html = res.read().decode('utf-8', errors='ignore')

# find "videoId":
vids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
print(f"Total videoId occurrences: {len(vids)}")
print(f"Sample videoIds: {list(dict.fromkeys(vids))[:15]}")
