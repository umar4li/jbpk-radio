import json
import urllib.request
import urllib.parse
import re
from concurrent.futures import ThreadPoolExecutor

with open('public/tracks.json', 'r', encoding='utf-8') as f:
    tracks = json.load(f)

print(f"Auditing {len(tracks)} tracks...")

bad_keywords = ['making', 'teaser', 'trailer', 'promo', 'status', 'short', 'behind the scene', 'dialogue']

def audit_track(item):
    idx, t = item
    vid = t.get('youtubeId')
    url = f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={vid}'
    issues = []
    yt_title = ""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3.5) as res:
            data = json.loads(res.read().decode())
            yt_title = data.get('title') or ""
            if not yt_title:
                issues.append("missing_title")
            else:
                low = yt_title.lower()
                for b in bad_keywords:
                    if b in low:
                        issues.append(f"bad_keyword:{b}")
                        break
    except Exception as e:
        issues.append(f"fetch_error:{e}")

    # Check embed restriction
    embed_url = f'https://www.youtube.com/embed/{vid}'
    try:
        er = urllib.request.Request(embed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(er, timeout=3.5) as ep:
            html = ep.read().decode('utf-8', errors='ignore')
            if 'UNPLAYABLE' in html or 'Playback on other websites has been disabled' in html:
                issues.append("unplayable_embed")
    except Exception as e:
        issues.append("embed_network_error")

    return idx, t, yt_title, issues

indexed = list(enumerate(tracks))
with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(audit_track, indexed))

problematic = [r for r in results if r[3]]
print(f"\nTotal problematic tracks found: {len(problematic)} out of {len(tracks)}")
for idx, t, yt_title, issues in problematic[:30]:
    print(f"#{idx+1} '{t['title']}' -> Issues: {issues} | YouTube Title: {yt_title}")

with open('problematic_tracks.json', 'w', encoding='utf-8') as f:
    json.dump([{'idx': r[0], 'song': r[1], 'yt_title': r[2], 'issues': r[3]} for r in problematic], f, indent=2)
