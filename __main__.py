# script to download custom songs from ragnarock
# you can choose the number of votes and rating below
#
# i'm @frozax on github and twitter. If you want to support me, just have a look at my games at https://www.frozax.com (mobile and steam)
# i'm prozero in-game and on the discord of ragnarock and ragnasongs

import json
import shutil
from pathlib import Path
import requests
import colorama
from pprint import pprint
import zipfile
from io import BytesIO
import string

# Conf
REQ_RATIO = 0.8

RAGNASONG_API_ENDPOINT = "https://ragnasong.com/api/searchMap/?start={start}&dificulty="
RAGNASONG_SONG = "https://ragnasong.com/api/map/{id}.zip"
SONGS_PER_PAGE = 10

custom_songs_path = Path("~/Documents").expanduser() / "Ragnarock" / "CustomSongs"
config = json.load(open("config.json"))

def err(s):
    print(colorama.Fore.RED + s + colorama.Style.RESET_ALL)

def warn(s):
    print(colorama.Fore.YELLOW + s + colorama.Style.RESET_ALL)

def ok(s):
    print(colorama.Fore.GREEN + s + colorama.Style.RESET_ALL)

def verbose(s):
    if config["verbose"]:
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
    downloaded_songs.append(f.name)

ok(f"Currently installed Songs: {len(downloaded_songs)}")
while True:
    ok(f"Downloading songs {start}-{start+9}")
    url = RAGNASONG_API_ENDPOINT.format(start=start)
    r = requests.get(url)
    d = r.json()
    if total == 0:
        total = d["count"]
        ok(f"Ragnasongs.com Songs count: {total}")
    for song in d["results"]:
        song_name = f"{song['artist']} - {song['title']}"
        song_id = int(song["id"])
        song_folder_name = ""
        for c in song['title'].lower():
            if c in string.ascii_lowercase:
                song_folder_name += c

        if song_folder_name in downloaded_songs:
            verbose(f"[ALREADY DOWNLOADED] {song_name}")
            if song_folder_name in config["ignored_songs"]:
                ok(f"[REMOVING] {song_name}")
                shutil.rmtree(custom_songs_path / song_folder_name)
            continue

        if song_folder_name in config["ignored_songs"]:
            verbose(f"[IGNORED] {song_name}")
            continue

        votes = song['downVotes'] + song['upVotes']
        if votes < config["min_votes"]:
            verbose(f"[NOT ENOUGH VOTES {votes}/{config['min_votes']}] {song_name}")
            continue
        ratio = song['upVotes'] / votes
        if ratio < config["good_bad_ratio"]:
            verbose(f"[RATING TOO LOW {ratio}/{config['good_bad_ratio']}] {song_name}")
            continue
        ok(f"[DOWNLOADING...] {song_name}")
        url_song = RAGNASONG_SONG.format(id=song_id)
        r_song = requests.get(url_song)
        with zipfile.ZipFile(BytesIO(r_song.content)) as zf:
            folder_name = custom_songs_path / song_folder_name
            folder_name.mkdir()
            verbose(f"[EXTRACTING...] in {folder_name}")
            for f_in_zip in zf.namelist():
                splitted = f_in_zip.split('/')
                if len(splitted) == 2:
                    fname = splitted[-1]
                elif len(splitted) == 1:
                    fname = splitted[0]
                elif len(splitted) == 3:
                    err(f"weird file: {f_in_zip}, ignored")
                    fname = ""
                else:
                    assert False, f"{splitted} should be length=2 (from {f_in_zip})"
                if fname != "":
                    with zf.open(f_in_zip) as f_in_zip_f:
                        (folder_name / splitted[-1]).open('wb').write(f_in_zip_f.read())

    start += SONGS_PER_PAGE
    if start >= total:
        ok("=> End")
        break