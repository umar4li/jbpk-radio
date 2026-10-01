import urllib.request
import re
import json

url = "https://www.youtube.com/playlist?list=PL-4vYzWm1VTRt8cjl5B9XVnnAsGtTHoKf"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

m = re.search(r'var ytInitialData = ({.*?});</script>', html)
if not m:
    m = re.search(r'ytInitialData\s*=\s*({.+?});', html)

if m:
    data = json.loads(m.group(1))
    keys = []
    def find_renderers(d):
        if isinstance(d, dict):
            for k in d.keys():
                if 'Renderer' in k:
                    keys.append(k)
            for v in d.values():
                find_renderers(v)
        elif isinstance(d, list):
            for x in d:
                find_renderers(x)
    find_renderers(data)
    print("Renderer types found:", set(keys))
