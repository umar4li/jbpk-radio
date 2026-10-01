import urllib.request
import json
import re

playlist_url = 'https://www.youtube.com/playlist?list=PL-4vYzWm1VTRt8cjl5B9XVnnAsGtTHoKf'
req = urllib.request.Request(playlist_url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
})

try:
    with urllib.request.urlopen(req, timeout=10) as res:
        html = res.read().decode('utf-8', errors='ignore')
        
    print("Fetched playlist HTML, length:", len(html))
    
    # Extract ytInitialData
    m = re.search(r'var ytInitialData = ({.*?});</script>', html)
    if not m:
        m = re.search(r'ytInitialData\s*=\s*({.+?});', html)
    
    if m:
        data = json.loads(m.group(1))
        # Search for playlistVideoRenderer
        videos = []
        def find_videos(obj):
            if isinstance(obj, dict):
                if 'playlistVideoRenderer' in obj:
                    pvr = obj['playlistVideoRenderer']
                    vid = pvr.get('videoId')
                    title = pvr.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
                    author = pvr.get('shortBylineText', {}).get('runs', [{}])[0].get('text', '')
                    length = pvr.get('lengthText', {}).get('simpleText', '')
                    videos.append({'videoId': vid, 'title': title, 'author': author, 'length': length})
                for v in obj.values():
                    find_videos(v)
            elif isinstance(obj, list):
                for item in obj:
                    find_videos(item)
        find_videos(data)
        print(f"Found {len(videos)} videos in playlist PL-4vYzWm1VTRt8cjl5B9XVnnAsGtTHoKf:")
        for idx, v in enumerate(videos[:15]):
            print(f"{idx+1}. {v['videoId']} - {v['title']} ({v['author']}) [{v['length']}]")
    else:
        print("ytInitialData not found, trying regex for videoId...")
        vids = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)
        print("Raw vids found:", len(vids), set(vids[:10]))
except Exception as e:
    print("Error:", e)
