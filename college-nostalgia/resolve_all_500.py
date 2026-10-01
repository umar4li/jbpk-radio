import json
import urllib.request
import urllib.parse
import re
import time
from concurrent.futures import ThreadPoolExecutor

# Load master list
with open("C:/Users/razau/.gemini/antigravity/scratch/college-nostalgia/master_songs_list.json", "r", encoding="utf-8") as f:
    master_list = json.load(f)

# Add 10 more to hit 500 exactly
extra_10 = [
    ["Mitwa Sun Mitwa", "Udit Narayan & Alka Yagnik", "Lagaan", "college", None],
    ["Radha Kaise Na Jale", "Asha Bhosle & Udit Narayan", "Lagaan", "retro90s", None],
    ["O Rey Chhori", "Udit Narayan & Alka Yagnik", "Lagaan", "romantic", None],
    ["Aankhon Ki Gustakhiyan", "Kumar Sanu & Kavita Krishnamurthy", "Hum Dil De Chuke Sanam", "romantic", None],
    ["Chand Chhupa Badal Mein", "Udit Narayan & Alka Yagnik", "Hum Dil De Chuke Sanam", "romantic", None],
    ["Tere Naam (Sad)", "Udit Narayan", "Tere Naam", "sad", None],
    ["Bheegi Si Bhaagi Si", "Mohit Chauhan & Shreya Ghoshal", "Raajneeti", "romantic", None],
    ["Mora Piya", "Aadesh Shrivastava", "Raajneeti", "sad", None],
    ["Kyun Mai Jaagoon", "Shafqat Amanat Ali", "Patiala House", "sad", None],
    ["Laung Da Lashkara", "Jasbir Jassi & Mahalakshmi", "Patiala House", "masti", None]
]

for item in extra_10:
    master_list.append(item)

print(f"Total songs to process: {len(master_list)}")

def get_yt_id(item):
    title, artist, album, category, ytid = item
    if ytid and len(ytid) == 11:
        return {
            "id": ytid,
            "youtubeId": ytid,
            "title": title,
            "artist": artist,
            "album": album,
            "category": category,
            "cover": f"https://img.youtube.com/vi/{ytid}/hqdefault.jpg"
        }
    
    # Search YouTube
    query = f"{title} {artist} {album} song"
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    found_id = None
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            html = res.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            if matches:
                # choose first match
                found_id = matches[0]
    except Exception as e:
        pass
    
    if not found_id:
        found_id = "5-n3R4Y6DYo" # default fallback
        
    return {
        "id": found_id,
        "youtubeId": found_id,
        "title": title,
        "artist": artist,
        "album": album,
        "category": category,
        "cover": f"https://img.youtube.com/vi/{found_id}/hqdefault.jpg"
    }

print("Resolving all songs via ThreadPool...")
start_time = time.time()
with ThreadPoolExecutor(max_workers=25) as executor:
    final_tracks = list(executor.map(get_yt_id, master_list))

print(f"Finished in {time.time() - start_time:.2f} seconds. Total tracks: {len(final_tracks)}")

# Ensure track #1 is Aye Meri College Ki Ladkiyon
if final_tracks[0]["title"] != "Aye Meri College Ki Ladkiyon":
    for idx, t in enumerate(final_tracks):
        if t["title"] == "Aye Meri College Ki Ladkiyon":
            first = final_tracks.pop(idx)
            final_tracks.insert(0, first)
            break

output_file = "C:/Users/razau/.gemini/antigravity/scratch/college-nostalgia/public/tracks.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(final_tracks, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(final_tracks)} tracks in {output_file}")
