import urllib.request
import json
import re

vids = [
    ('8', 'iEpHUkH61rU'),
    ('1', 'EBoV6-MrvNs'),
    ('2', 'RNXYQ-LViAI'),
    ('3', 'qsNAD6gFIEk'),
    ('4', 'ceqt8IlnYUg'),
    ('5', 'cn84fZBjgnI'),
    ('6', 'SQ4jZ-EAL88'),
    ('7', 'm6Y8xEfyXTs')
]

print("--- Checking direct videos ---")
for num, v in vids:
    try:
        url = f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={v}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read())
            title = data.get('title', 'Unknown')
            author = data.get('author_name', 'Unknown')
            print(f"[{num}] {v} => {title} ({author})")
    except Exception as e:
        print(f"[{num}] {v} => Error: {e}")
