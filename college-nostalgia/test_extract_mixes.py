import urllib.request
import re
import json

urls = [
    ("Mix 1 (Tera Naam Doon)", "https://www.youtube.com/watch?v=EBoV6-MrvNs&list=RDEBoV6-MrvNs"),
    ("Mix 2 (Nazar Lagi)", "https://www.youtube.com/watch?v=RNXYQ-LViAI&list=RDRNXYQ-LViAI"),
    ("Mix 3 (Kisi Se Tum Pyar Karo)", "https://www.youtube.com/watch?v=qsNAD6gFIEk&list=RDGMEMCMFH2exzjBeE_zAHHJOdxg"),
    ("Mix 4 (Dil Leke Darde Dil)", "https://www.youtube.com/watch?v=ceqt8IlnYUg&list=RDceqt8IlnYUg"),
    ("Mix 5 (Hun Ishq Main)", "https://www.youtube.com/watch?v=cn84fZBjgnI&list=RDcn84fZBjgnI"),
    ("Playlist 7 (Veer-Zaara & Bollywood)", "https://www.youtube.com/playlist?list=PL-4vYzWm1VTRt8cjl5B9XVnnAsGtTHoKf")
]

for label, u in urls:
    req = urllib.request.Request(u, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            html = res.read().decode('utf-8', errors='ignore')
            vids = list(dict.fromkeys(re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)))
            print(f"{label}: found {len(vids)} unique videoIds: {vids[:5]}")
    except Exception as e:
        print(f"{label}: error {e}")
