import urllib.request
import urllib.parse
import json

songs_data = [
    {
        "id": "5-n3R4Y6DYo",
        "youtubeId": "5-n3R4Y6DYo",
        "title": "Aye Meri College Ki Ladkiyon",
        "artist": "Udit Narayan",
        "album": "Yeh Dil Aashiqana",
        "query": "College Ki Ladkiyon Yeh Dil Aashiqana Udit Narayan"
    },
    {
        "id": "69K83b7zV6k",
        "youtubeId": "69K83b7zV6k",
        "title": "Koi Kahe Kehta Rahe",
        "artist": "Shankar Mahadevan, Shaan & KK",
        "album": "Dil Chahta Hai",
        "query": "Koi Kahe Kehta Rahe Dil Chahta Hai"
    },
    {
        "id": "1X73p3iY7YI",
        "youtubeId": "1X73p3iY7YI",
        "title": "Papa Kehte Hain Bada Naam Karega",
        "artist": "Udit Narayan",
        "album": "Qayamat Se Qayamat Tak",
        "query": "Papa Kehte Hain Qayamat Se Qayamat Tak"
    },
    {
        "id": "qZq6Kq5N8lA",
        "youtubeId": "qZq6Kq5N8lA",
        "title": "Pehla Nasha",
        "artist": "Udit Narayan & Sadhana Sargam",
        "album": "Jo Jeeta Wohi Sikandar",
        "query": "Pehla Nasha Jo Jeeta Wohi Sikandar"
    },
    {
        "id": "bC7KkG9lU3k",
        "youtubeId": "bC7KkG9lU3k",
        "title": "Yaaron Dosti Badi Hi Haseen Hai",
        "artist": "KK",
        "album": "Rockford / Pal",
        "query": "Yaaron KK Rockford"
    },
    {
        "id": "6PqJ1vO2g5w",
        "youtubeId": "6PqJ1vO2g5w",
        "title": "Woh Pehli Baar Jab Hum Mile",
        "artist": "Shaan",
        "album": "Pyaar Mein Kabhi Kabhi",
        "query": "Woh Pehli Baar Shaan Pyaar Mein Kabhi Kabhi"
    },
    {
        "id": "QZ7gW8Z_PjU",
        "youtubeId": "QZ7gW8Z_PjU",
        "title": "Purani Jeans Aur Guitar",
        "artist": "Ali Haider",
        "album": "Purani Jeans",
        "query": "Purani Jeans Ali Haider"
    },
    {
        "id": "gpe61_s_q3w",
        "youtubeId": "gpe61_s_q3w",
        "title": "Woh Din Bhi Kya Din The",
        "artist": "Arijit Singh",
        "album": "Chhichhore",
        "query": "Woh Din Arijit Singh Chhichhore"
    },
    {
        "id": "6Na7GSV9bVY",
        "youtubeId": "6Na7GSV9bVY",
        "title": "Chura Ke Dil Mera",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Main Khiladi Tu Anari",
        "query": "Chura Ke Dil Mera Main Khiladi Tu Anari"
    },
    {
        "id": "3NWMK2MRqIk",
        "youtubeId": "3NWMK2MRqIk",
        "title": "Tumsa Koi Pyaara",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Khuddar",
        "query": "Tumsa Koi Pyaara Khuddar"
    },
    {
        "id": "f5b3K3m0P7Q",
        "youtubeId": "f5b3K3m0P7Q",
        "title": "Main Koi Aisa Geet Gaoon",
        "artist": "Abhijeet & Alka Yagnik",
        "album": "Yes Boss",
        "query": "Main Koi Aisa Geet Gaoon Yes Boss Abhijeet"
    },
    {
        "id": "8QnZ2fBqK4c",
        "youtubeId": "8QnZ2fBqK4c",
        "title": "Gori Gori",
        "artist": "KK, Sunidhi Chauhan, Anu Malik",
        "album": "Main Hoon Na",
        "query": "Gori Gori Main Hoon Na"
    },
    {
        "id": "v5Yn1aK_8tE",
        "youtubeId": "v5Yn1aK_8tE",
        "title": "Yeh Ladka Hai Deewana",
        "artist": "Udit Narayan & Alka Yagnik",
        "album": "Kuch Kuch Hota Hai",
        "query": "Yeh Ladka Hai Deewana Kuch Kuch Hota Hai"
    },
    {
        "id": "2g0T_2r1bPQ",
        "youtubeId": "2g0T_2r1bPQ",
        "title": "Aankhon Mein Base Ho Tum",
        "artist": "Alka Yagnik & Abhijeet",
        "album": "Takkar",
        "query": "Aankhon Mein Base Ho Tum Takkar Abhijeet"
    },
    {
        "id": "5y_TCKNzAMI",
        "youtubeId": "5y_TCKNzAMI",
        "title": "Tumse Milne Ko Dil",
        "artist": "Alka Yagnik & Kumar Sanu",
        "album": "Phool Aur Kaante",
        "query": "Tumse Milne Ko Dil Phool Aur Kaante"
    },
    {
        "id": "oFxbBeYhLqM",
        "youtubeId": "oFxbBeYhLqM",
        "title": "Saaton Janam Main Tere",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Dilwale",
        "query": "Saaton Janam Main Tere Dilwale"
    },
    {
        "id": "N0jnLZxYwYc",
        "youtubeId": "N0jnLZxYwYc",
        "title": "Mujhse Mohabbat Ka Izhaar Karta",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Hum Hain Rahi Pyar Ke",
        "query": "Mujhse Mohabbat Ka Izhaar Hum Hain Rahi Pyar Ke"
    },
    {
        "id": "zuPoUsdXrqM",
        "youtubeId": "zuPoUsdXrqM",
        "title": "Dheere Dheere Pyar Ko Badhana Hai",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Phool Aur Kaante",
        "query": "Dheere Dheere Pyar Ko Badhana Kumar Sanu Alka Yagnik"
    },
    {
        "id": "wV8njoRVefQ",
        "youtubeId": "wV8njoRVefQ",
        "title": "Kitna Pyaara Tujhe Rabne Banaya",
        "artist": "Alka Yagnik & Udit Narayan",
        "album": "Raja Hindustani",
        "query": "Kitna Pyaara Tujhe Rabne Banaya Raja Hindustani"
    },
    {
        "id": "rXHY4Cv9cA8",
        "youtubeId": "rXHY4Cv9cA8",
        "title": "Ab Tere Bin Ji Lenge Hum",
        "artist": "Kumar Sanu",
        "album": "Aashiqui",
        "query": "Ab Tere Bin Ji Lenge Hum Aashiqui"
    },
    {
        "id": "htMvfOfixuM",
        "youtubeId": "htMvfOfixuM",
        "title": "Ek Ladki Ko Dekha",
        "artist": "Kumar Sanu",
        "album": "1942 A Love Story",
        "query": "Ek Ladki Ko Dekha 1942 A Love Story"
    },
    {
        "id": "nNhv8A_rJTg",
        "youtubeId": "nNhv8A_rJTg",
        "title": "Oye Raju Pyar Na Kariyo",
        "artist": "Anand Raj Anand",
        "album": "Hadh Kar Di Aapne",
        "query": "Oye Raju Pyar Na Kariyo Hadh Kar Di Aapne"
    },
    {
        "id": "fRrk7xVw7iA",
        "youtubeId": "fRrk7xVw7iA",
        "title": "Chand Sitare Phool Aur Khushboo",
        "artist": "Kumar Sanu",
        "album": "Kaho Naa... Pyaar Hai",
        "query": "Chand Sitare Kaho Naa Pyaar Hai"
    },
    {
        "id": "BaAoZA0fup0",
        "youtubeId": "BaAoZA0fup0",
        "title": "Dil Ka Aalam",
        "artist": "Kumar Sanu",
        "album": "Aashiqui",
        "query": "Dil Ka Aalam Main Kya Batau Kumar Sanu Aashiqui"
    },
    {
        "id": "cBGDDBHN22U",
        "youtubeId": "cBGDDBHN22U",
        "title": "Pehli Pehli Baar Mohabbat Ki Hai",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Sirf Tum",
        "query": "Pehli Pehli Baar Mohabbat Ki Hai Sirf Tum"
    },
    {
        "id": "yL9x7lWq4fM",
        "youtubeId": "yL9x7lWq4fM",
        "title": "Dil Chahta Hai",
        "artist": "Shankar Mahadevan",
        "album": "Dil Chahta Hai",
        "query": "Dil Chahta Hai Title Track Shankar Mahadevan"
    },
    {
        "id": "YOYN9qNXmAw",
        "youtubeId": "YOYN9qNXmAw",
        "title": "Chaiyya Chaiyya",
        "artist": "Sukhwinder Singh & Sapna Awasthi",
        "album": "Dil Se",
        "query": "Chaiyya Chaiyya Sukhwinder Singh Dil Se"
    },
    {
        "id": "Jb2t0A1Xp3w",
        "youtubeId": "Jb2t0A1Xp3w",
        "title": "Masti Ki Pathshala",
        "artist": "Naresh Iyer & A.R. Rahman",
        "album": "Rang De Basanti",
        "query": "Pathshala Loose Control Rang De Basanti"
    },
    {
        "id": "CTuvMubzXpU",
        "youtubeId": "CTuvMubzXpU",
        "title": "Jeeta Tha Jiske Liye",
        "artist": "Kumar Sanu & Alka Yagnik",
        "album": "Dilwale",
        "query": "Jeeta Tha Jiske Liye Dilwale Kumar Sanu"
    },
    {
        "id": "otQmzlm-s7Q",
        "youtubeId": "otQmzlm-s7Q",
        "title": "Main Duniya Bhula Doonga",
        "artist": "Kumar Sanu & Anuradha Paudwal",
        "album": "Aashiqui",
        "query": "Main Duniya Bhula Doonga Aashiqui"
    }
]

curated_tracks = []

for idx, s in enumerate(songs_data):
    q = urllib.parse.quote(s["query"])
    url = f"https://itunes.apple.com/search?term={q}&country=IN&media=music&limit=1"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    item = {
        "id": s["youtubeId"],
        "youtubeId": s["youtubeId"],
        "title": s["title"],
        "artist": s["artist"],
        "album": s["album"],
        "cover": "",
        "previewUrl": ""
    }
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            if data.get("results"):
                res = data["results"][0]
                item["cover"] = res.get("artworkUrl100", "").replace("100x100bb", "600x600bb")
                item["previewUrl"] = res.get("previewUrl", "")
    except Exception as e:
        pass
        
    if not item["cover"]:
        item["cover"] = f"https://img.youtube.com/vi/{s['youtubeId']}/hqdefault.jpg"
        
    curated_tracks.append(item)

out_file = "C:/Users/razau/.gemini/antigravity/scratch/college-nostalgia/public/tracks.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(curated_tracks, f, ensure_ascii=False, indent=2)

print("Curated count:", len(curated_tracks))
