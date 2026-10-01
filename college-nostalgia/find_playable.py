import urllib.request
import urllib.parse
import re

query = 'Aye Meri College Ki Ladkiyon Yeh Dil Aashiqana'
url = f'https://www.youtube.com/results?search_query={urllib.parse.quote(query)}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=5) as res:
    html = res.read().decode('utf-8', errors='ignore')
    matches = list(set(re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)))
    print('Found candidate IDs:', matches[:8])

for vid in matches[:8]:
    embed_url = f'https://www.youtube.com/embed/{vid}'
    r = urllib.request.Request(embed_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(r, timeout=4) as ep:
            body = ep.read().decode('utf-8', errors='ignore')
            unplayable = 'UNPLAYABLE' in body or 'Playback on other websites has been disabled' in body
            print(f'{vid}: Unplayable={unplayable}')
    except Exception as e:
        print(f'{vid}: err {e}')
