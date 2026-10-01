import urllib.request
import re
import json

mix_urls = [
    ("track8", "Track 8 (College Ki Ladkiyon)", ["iEpHUkH61rU"]),
    ("mix1", "Tera Naam Doon (Slowed)", "https://www.youtube.com/watch?v=EBoV6-MrvNs&list=RDEBoV6-MrvNs"),
    ("mix2", "Nazar Lagi & Melodies", "https://www.youtube.com/watch?v=RNXYQ-LViAI&list=RDRNXYQ-LViAI"),
    ("mix3", "Kisi Se Tum Pyar Karo (Lofi)", "https://www.youtube.com/watch?v=qsNAD6gFIEk&list=RDGMEMCMFH2exzjBeE_zAHHJOdxg"),
    ("mix4", "Dil Leke Darde Dil (Reverb)", "https://www.youtube.com/watch?v=ceqt8IlnYUg&list=RDceqt8IlnYUg"),
    ("mix5", "Hun Ishq Main (Atif Aslam)", "https://www.youtube.com/watch?v=cn84fZBjgnI&list=RDcn84fZBjgnI"),
    ("track6", "Vaaroon Forever", ["SQ4jZ-EAL88"]),
    ("playlist7", "YRF & Bollywood Hits", "https://www.youtube.com/playlist?list=PL-4vYzWm1VTRt8cjl5B9XVnnAsGtTHoKf")
]

all_extracted = []

def extract_from_html(html, category_name):
    # Regex for video items in playlist/mix
    # Typical pattern in ytInitialData:
    # "videoId":"...","thumbnail":{"thumbnails":[...]},"title":{"runs":[{"text":"..."}]},"longBylineText":{"runs":[{"text":"..."}]}
    items = []
    # Let's search ytInitialData block
    m = re.search(r'var ytInitialData = ({.*?});</script>', html)
    if not m:
        m = re.search(r'ytInitialData\s*=\s*({.+?});', html)
    
    if m:
        data = json.loads(m.group(1))
        # Traverse dictionary
        def walk(d):
            if isinstance(d, dict):
                # Check for playlistPanelVideoRenderer (used in Mixes/Radios)
                if 'playlistPanelVideoRenderer' in d:
                    r = d['playlistPanelVideoRenderer']
                    vid = r.get('videoId')
                    title = r.get('title', {}).get('simpleText') or (r.get('title', {}).get('runs', [{}])[0].get('text', ''))
                    byline = r.get('longBylineText', {}).get('runs', [{}])[0].get('text', '') or r.get('shortBylineText', {}).get('runs', [{}])[0].get('text', '')
                    if vid and title:
                        items.append({'youtubeId': vid, 'title': title, 'artist': byline, 'category': category_name})
                # Check for playlistVideoRenderer (used in Playlists)
                elif 'playlistVideoRenderer' in d:
                    r = d['playlistVideoRenderer']
                    vid = r.get('videoId')
                    title = r.get('title', {}).get('runs', [{}])[0].get('text', '') or r.get('title', {}).get('simpleText', '')
                    byline = r.get('shortBylineText', {}).get('runs', [{}])[0].get('text', '')
                    if vid and title:
                        items.append({'youtubeId': vid, 'title': title, 'artist': byline, 'category': category_name})
                for v in d.values():
                    walk(v)
            elif isinstance(d, list):
                for x in d:
                    walk(x)
        walk(data)
    return items

results = {}
for key, cat, target in mix_urls:
    if isinstance(target, list):
        results[key] = [{'youtubeId': vid, 'category': cat} for vid in target]
    else:
        req = urllib.request.Request(target, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                items = extract_from_html(html, cat)
                results[key] = items
                print(f"[{cat}] Found {len(items)} structured songs!")
        except Exception as e:
            print(f"Error fetching {cat}: {e}")

with open('extracted_user_tracks.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved structured extraction to extracted_user_tracks.json")
