import urllib.request
import urllib.parse
import re

query = 'Kaho Naa Pyaar Hai full lyrical song Hrithik Roshan'
url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(query)}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=4) as res:
    html = res.read().decode('utf-8', errors='ignore')
    matches = list(set(re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)))

for vid in matches[:8]:
    embed_url = f'https://www.youtube.com/embed/{vid}'
    er = urllib.request.Request(embed_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(er, timeout=4) as ep:
            body = ep.read().decode('utf-8', errors='ignore')
            unp = 'UNPLAYABLE' in body or 'Playback on other websites has been disabled' in body
            print(vid, 'unplayable:', unp)
            if not unp:
                print('Found playable ID for Kaho Naa Pyaar Hai:', vid)
                break
    except Exception as e:
        print(f"Error {vid}: {e}")
