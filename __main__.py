import sys
from pathlib import Path
import requests
import colorama
from pprint import pprint

# Conf
#STEAM_PARENT_FOLDER = "D:\\Program Files (x86)"
RAGNASONG_API_ENDPOINT = "https://ragnasong.com/api/searchMap/?start={start}&difficulty="
SONGS_PER_PAGE = 10

def error(msg):
    print(msg)
    sys.exit(1)

#ragnarock_path = Path(STEAM_PARENT_FOLDER) / "Steam" / "steamapps" / "Ragnarock"
#if not ragnarock_path.exists():
#    error(f"Can't find Ragnarock folder at {ragnarock_path}")
#
custom_songs_path = Path("C:\\Users\Francois\Documents") / "Ragnarock" / "CustomSongs"

def err(s):
    print(colorama.Fore.RED + s + colorama.Style.RESET_ALL)

def warn(s):
    print(colorama.Fore.YELLOW + s + colorama.Style.RESET_ALL)

def ok(s):
    print(colorama.Fore.GREEN + s + colorama.Style.RESET_ALL)

def debug(s):
    print(s)

warn("warn")
err("err")
ok("ok")
debug("debug")

if not custom_songs_path.exists():
    warn(f"Create custom songs path {custom_songs_path}")
    custom_songs_path.mkdir(parents=True)

start = 0
while True:
    url = RAGNASONG_API_ENDPOINT.format(start=start)
    pprint(url)
    r = requests.get(url)
    pprint(r)
    pprint(r.text)
    pprint(r.json())
    break