import urllib.request
import urllib.parse
import re

def search_yt_id(query):
    try:
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=5) as res:
            html = res.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            for m in matches:
                # filter out obvious shorts or ads if possible
                return m
    except Exception as e:
        print(f"Error searching {query}: {e}")
    return None

test_id = search_yt_id("Aye Meri College Ki Ladkiyon Yeh Dil Aashiqana")
print("Found test ID:", test_id)
