import requests
import json
from data_managers.data_loader import DataLoader
from main import readJSON

def writeJSON(file, key, new_data):
    with open(file, "r") as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        data[key] = new_data
    else:
        data = {key: new_data}

    with open(file, "w") as f:
        json.dump(data, f, indent=2)

#base API url
url = "https://itunes.apple.com/search"

#read existing data 
songs = DataLoader.read_json("songs.json", 'songs')
#songs = readJSON("songs.json", 'songs')
artists = DataLoader.read_json("artists.json", 'artists') 
#artists = readJSON("artists.json", 'artists') 

#-------- FILLLING SONG URLS ---------------------------------------------------------
for song in songs:
    print(f"Searching image for: {song['title']} by {song['artist']}")
    query = f"{song['title']} {song['artist']}"
    params = {
        "term": query,
        "media": "music",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params)
        results = response.json()

        if results["resultCount"] > 0:
            imageUrl = results["results"][0]["artworkUrl100"]
            song["image"] = imageUrl.replace("100x100", "600x600")
        else:
            song["image"] = "images/record.jpg"
    except Exception as e:
        print(f"Failed to fetch image for {song['title']}: {e}")
        song["image"] = "images/record.jpg"

# write once after all songs are updated
DataLoader.write_json("songs.json", "songs", songs)
#writeJSON("songs.json", "songs", songs)

print("song urls filled")
#-------- EOF SONG URLS ---------------------------------------------------------------

#-------- FILLLING ARTIST URLS ---------------------------------------------------------
for artist in artists:
    print(f"Searching image for: {artist['artist']}")
    query = f"{artist['artist']}"
    params = {
        "term": query,
        "media": "music",
        "limit": 1
    }

    try:
        response = requests.get(url, params=params)
        results = response.json()

        if results["resultCount"] > 0:
            imageUrl = results["results"][0]["artworkUrl100"]
            artist["image"] = imageUrl.replace("100x100", "600x600")
        else:
            artist["image"] = "images/record.jpg"
    except Exception as e:
        print(f"Failed to fetch image for {artist['artist']}: {e}")
        artist["image"] = "images/noProfile.jpg"

DataLoader.write_json("artists.json", "artists", artists)
#writeJSON("artists.json", "artists", artists)

print("artist urls filled")
#-------- EOF ARTIST URLS ---------------------------------------------------------------
