import json
from json.decoder import JSONDecodeError

filename = "guilds.json"

global Config

def open_conf():
    global config
    try:
        with open(filename) as f:
            config = json.load(f)
    except JSONDecodeError as e:
        print(e)
        config = {}


def save_conf():
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)
