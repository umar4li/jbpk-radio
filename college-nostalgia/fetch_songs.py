import urllib.request
import urllib.parse
import json
import os

songs_input = [
    {
        "title": "Aye Meri College Ki Ladkiyon",
        "query": "College Ki Ladkiyon Yeh Dil Aashiqana Udit Narayan",
        "youtubeId": "5-n3R4Y6DYo",
        "artist": "Udit Narayan",
        "album": "Yeh Dil Aashiqana"
    },
    {
        "title": "Koi Kahe Kehta Rahe",
        "query": "Koi Kahe Kehta Rahe Dil Chahta Hai",
        "youtubeId": "69K83b7zV6k",
        "artist": "Shankar Mahadevan, Shaan, KK",
        "album": "Dil Chahta Hai"
    },
    {
        "title": "Papa Kehte Hain Bada Naam Karega",
        "query": "Papa Kehte Hain Qayamat Se Qayamat Tak",
        "youtubeId": "1X73p3iY7YI",
        "artist": "Udit Narayan",
        "album": "Qayamat Se Qayamat Tak"
    },
    {
        "title": "Pehla Nasha",
        "query": "Pehla Nasha Jo Jeeta Wohi Sikandar",
        "youtubeId": "qZq6Kq5N8lA",
        "artist": "Udit Narayan & Sadhana Sargam",
        "album": "Jo Jeeta Wohi Sikandar"
    },
    {
        "title": "Yaaron Dosti Badi Hi Haseen Hai",
        "query": "Yaaron KK Rockford",
        "youtubeId": "bC7KkG9lU3k",
        "artist": "KK",
        "album": "Pal (Rockford)"
    },
    {
        "title": "Woh Pehli Baar Jab Hum Mile",
        "query": "Woh Pehli Baar Shaan Pyaar Mein Kabhi Kabhi",
        "youtubeId": "6PqJ1vO2g5w",
        "artist": "Shaan",
        "album": "Pyaar Mein Kabhi Kabhi"
    },
    {
        "title": "Purani Jeans Aur Guitar",
        "query": "Purani Jeans Ali Haider",
        "youtubeId": "QZ7gW8Z_PjU",
        "artist": "Ali Haider",
        "album": "Sandesa"
    },
    {
        "title": "Woh Din Bhi Kya Din The",
        "query": "Woh Din Arijit Singh Chhichhore",
        "youtubeId": "gpe61_s_q3w",
        "artist": "Arijit Singh",
        "album": "Chhichhore"
    },
    {
        "title": "Chura Ke Dil Mera",
        "query": "Chura Ke Dil Mera Main Khiladi Tu Anari",
        "youtubeId": "6Na7GSV9bVY",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Main Khiladi Tu Anari"
    },
    {
        "title": "Tumsa Koi Pyaara",
        "query": "Tumsa Koi Pyaara Khuddar",
        "youtubeId": "3NWMK2MRqIk",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Khuddar"
    },
    {
        "title": "Main Koi Aisa Geet Gaoon",
        "query": "Main Koi Aisa Geet Gaoon Yes Boss Abhijeet",
        "youtubeId": "f5b3K3m0P7Q",
        "artist": "Abhijeet Bhattacharya & Alka Yagnik",
        "album": "Yes Boss"
    },
    {
        "title": "Gori Gori",
        "query": "Gori Gori Main Hoon Na",
        "youtubeId": "8QnZ2fBqK4c",
        "artist": "KK, Sunidhi Chauhan, Anu Malik",
        "album": "Main Hoon Na"
    },
    {
        "title": "Aankhon Mein Base Ho Tum",
        "query": "Aankhon Mein Base Ho Tum Takkar",
        "youtubeId": "2g0T_2r1bPQ",
        "artist": "Abhijeet & Alka Yagnik",
        "album": "Takkar"
    },
    {
        "title": "Tumse Milne Ko Dil",
        "query": "Tumse Milne Ko Dil Phool Aur Kaante",
        "youtubeId": "5y_TCKNzAMI",
        "artist": "Alka Yagnik & Kumar Sanu",
        "album": "Phool Aur Kaante"
    },
    {
        "title": "Saaton Janam Main Tere",
        "query": "Saaton Janam Main Tere Dilwale",
        "youtubeId": "oFxbBeYhLqM",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Dilwale"
    },
    {
        "title": "Mujhse Mohabbat Ka Izhaar Karta",
        "query": "Mujhse Mohabbat Ka Izhaar Karta Hum Hain Rahi Pyar Ke",
        "youtubeId": "N0jnLZxYwYc",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Hum Hain Rahi Pyar Ke"
    },
    {
        "title": "Dheere Dheere Pyar Ko Badhana Hai",
        "query": "Dheere Dheere Pyar Ko Badhana Hai Phool Aur Kaante",
        "youtubeId": "zuPoUsdXrqM",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Phool Aur Kaante"
    },
    {
        "title": "Kitna Pyaara Tujhe Rabne Banaya",
        "query": "Kitna Pyaara Tujhe Rabne Banaya Raja Hindustani",
        "youtubeId": "wV8njoRVefQ",
        "artist": "Alka Yagnik & Udit Narayan",
        "album": "Raja Hindustani"
    },
    {
        "title": "Ab Tere Bin Ji Lenge Hum",
        "query": "Ab Tere Bin Ji Lenge Hum Aashiqui",
        "youtubeId": "rXHY4Cv9cA8",
        "artist": "Kumar Sanu",
        "album": "Aashiqui"
    },
    {
        "title": "Ek Ladki Ko Dekha",
        "query": "Ek Ladki Ko Dekha 1942 A Love Story",
        "youtubeId": "htMvfOfixuM",
        "artist": "Kumar Sanu",
        "album": "1942 A Love Story"
    },
    {
        "title": "Oye Raju Pyar Na Kariyo",
        "query": "Oye Raju Pyar Na Kariyo Hadh Kar Di Aapne",
        "youtubeId": "nNhv8A_rJTg",
        "artist": "Anand Raj Anand",
        "album": "Hadh Kar Di Aapne"
    },
    {
        "title": "Yeh Ladka Hai Deewana",
        "query": "Yeh Ladka Hai Deewana Kuch Kuch Hota Hai",
        "youtubeId": "v5Yn1aK_8tE",
        "artist": "Udit Narayan & Alka Yagnik",
        "album": "Kuch Kuch Hota Hai"
    },
    {
        "title": "Chand Sitare Phool Aur Khushboo",
        "query": "Chand Sitare Kaho Naa Pyaar Hai",
        "youtubeId": "fRrk7xVw7iA",
        "artist": "Kumar Sanu",
        "album": "Kaho Naa... Pyaar Hai"
    },
    {
        "title": "Dil Ka Aalam",
        "query": "Dil Ka Aalam Main Kya Batau Tujhe Aashiqui",
        "youtubeId": "BaAoZA0fup0",
        "artist": "Kumar Sanu",
        "album": "Aashiqui"
    },
    {
        "title": "Pehli Pehli Baar Mohabbat Ki Hai",
        "query": "Pehli Pehli Baar Mohabbat Ki Hai Sirf Tum",
        "youtubeId": "cBGDDBHN22U",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Sirf Tum"
    }
]

output_tracks = []

for idx, item in enumerate(songs_input):
    q = urllib.parse.quote(item["query"])
    url = f"https://itunes.apple.com/search?term={q}&country=IN&media=music&limit=1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    track = {
        "id": item["youtubeId"],
        "youtubeId": item["youtubeId"],
        "title": item["title"],
        "artist": item["artist"],
        "album": item["album"],
        "cover": "",
        "previewUrl": ""
    }
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode())
            if data.get("results"):
                res = data["results"][0]
                track["artist"] = res.get("artistName", item["artist"])
                track["album"] = res.get("collectionName", item["album"])
                track["cover"] = res.get("artworkUrl100", "").replace("100x100bb", "600x600bb")
                track["previewUrl"] = res.get("previewUrl", "")
                print(f"[{idx+1}/{len(songs_input)}] Matched: {track['title']} -> {track['artist']}")
            else:
                print(f"[{idx+1}/{len(songs_input)}] No iTunes match for {item['title']}, using fallback metadata.")
    except Exception as e:
        print(f"[{idx+1}/{len(songs_input)}] Err for {item['title']}: {e}")
    
    # If no cover, provide high quality fallback or youtube thumbnail
    if not track["cover"]:
        track["cover"] = f"https://img.youtube.com/vi/{item['youtubeId']}/hqdefault.jpg"
        
    output_tracks.append(track)

out_file = "C:/Users/razau/.gemini/antigravity/scratch/college-nostalgia/public/tracks.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(output_tracks, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(output_tracks)} tracks in {out_file}")
