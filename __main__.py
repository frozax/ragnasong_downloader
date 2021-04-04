import sys
from pathlib import Path
import requests
import colorama
from pprint import pprint
import zipfile
from io import BytesIO

# Conf
#STEAM_PARENT_FOLDER = "D:\\Program Files (x86)"
RAGNASONG_API_ENDPOINT = "https://ragnasong.com/api/searchMap/?start={start}&dificulty="
RAGNASONG_SONG = "https://ragnasong.com/api/map/{id}.zip"
SONGS_PER_PAGE = 10

def error(msg):
    print(msg)
    sys.exit(1)

custom_songs_path = Path("C:\\Users\\Francois\\Documents") / "Ragnarock" / "CustomSongs"
custom_songs_path = Path("D:\\gamedev\\tmp\\ragnarock")

def err(s):
    print(colorama.Fore.RED + s + colorama.Style.RESET_ALL)

def warn(s):
    print(colorama.Fore.YELLOW + s + colorama.Style.RESET_ALL)

def ok(s):
    print(colorama.Fore.GREEN + s + colorama.Style.RESET_ALL)

def debug(s):
    print(s)

if not custom_songs_path.exists():
    warn(f"Create custom songs path {custom_songs_path}")
    custom_songs_path.mkdir(parents=True)

start = 0
total = 0
downloaded_songs = []
for f in custom_songs_path.iterdir():
    if not f.is_dir():
        continue
    try:
        downloaded_songs.append(int(f.name))
    except ValueError:
        continue

ok(f"Currently installed Songs: {len(downloaded_songs)}")
while True:
    url = RAGNASONG_API_ENDPOINT.format(start=start)
    r = requests.get(url)
    d = r.json()
    if total == 0:
        total = d["count"]
        ok(f"Ragnasongs.com Songs count: {total}")
    for song in d["results"]:
        song_name = f"{song['artist']} - {song['title']}"
        song_id = int(song["id"])
        if song_id in downloaded_songs:
            ok(f"[ALREADY DOWNLOADED] {song_name}")
        else:
            warn(f"[DOWNLOADING...] {song_name}")
            url_song = RAGNASONG_SONG.format(id=song_id)
            r_song = requests.get(url_song)
            with zipfile.ZipFile(BytesIO(r_song.content)) as zf:
                zf.extractall(custom_songs_path / str(song_id))

        break

    start += SONGS_PER_PAGE
    if True: #start >= total:
        ok("=> End")
        break
    break