import json

with open('public/tracks.json', 'r', encoding='utf-8') as f:
    tracks = json.load(f)

for idx, t in enumerate(tracks):
    # First 164 tracks are from the user's provided links
    if idx < 164:
        t['isJbSpecial'] = True
    else:
        t['isJbSpecial'] = False

    cat = str(t.get('category', '')).lower()
    if 'slowed' in cat or 'lofi' in cat:
        t['category'] = 'slowed'
    elif 'romantic' in cat or 'love' in cat:
        t['category'] = 'romantic'
    elif 'veer-zaara' in cat or 'classic' in cat or 'retro' in cat or '90s' in cat:
        t['category'] = 'classic'
    elif 'college' in cat:
        t['category'] = 'college'
    elif 'masti' in cat or 'party' in cat:
        t['category'] = 'masti'
    elif 'sad' in cat or 'soulful' in cat:
        t['category'] = 'sad'
    elif 'jb top' in cat:
        t['category'] = 'jb_special'
    else:
        t['category'] = 'romantic'

with open('public/tracks.json', 'w', encoding='utf-8') as f:
    json.dump(tracks, f, ensure_ascii=False, indent=2)

print("Updated public/tracks.json with standardized categories and isJbSpecial flags!")
