import json
from json.decoder import JSONDecodeError

filename = "guilds.json"

Config = {}

def open_conf():
    global Config
    try:
        with open(filename) as f:
            Config = json.load(f)
    except JSONDecodeError as e:
        print(e)
        Config = {}


def save_conf():
    with open(filename, "w") as f:
        json.dump(Config, f, indent=4)
