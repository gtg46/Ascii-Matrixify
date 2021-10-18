import json
from json.decoder import JSONDecodeError
import sys
from typing import Callable, NoReturn
import argparse
from PIL import Image
magenta ="\x1b[38;5;57m"
cat_purp = "\x1b[38;2;73;47;146m"

def get_color_printer(r: str, g: str, b:str) -> Callable[[str, str, str], NoReturn]:
    ANSI_color = "\x1b[38;2;"
    ANSI_color += r + ";" + g + ";" + b + "m"
    def color_printer(value: str, end="\n"):
        print(ANSI_color, value, sep="", end=end)
    return color_printer


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()



def get_json(path: str) -> dict:

    loaded = None
    json_file = None

    try:
        json_file = open(path , 'r')
        loaded = json.load(json_file)

    except JSONDecodeError as e:
        print(path, "- Invalid JSON")

    except FileNotFoundError as e:
        print(path, "-",  e.strerror)
        
    finally:
        if json_file != None:
            json_file.close()

    return loaded


def parse_args(defaults: dict) -> dict:
    parser = argparse.ArgumentParser(defaults["description"])
    for setting in defaults["settings"]:
        parser.add_argument(
            *setting["flags"].split(),
            help=setting["help"],
            default=setting["default"]
        )

    return vars(parser.parse_args())

def configure() -> dict:
    DEFAULTS_PATH = "config/setup.json"
    setup = get_json(DEFAULTS_PATH)
    settings = parse_args(setup)


    if settings["config"] != DEFAULTS_PATH:
        config = get_json(settings["config"])

        if config != None:
            settings.update(config)

    return settings

def start(settings: dict) -> NoReturn:
    print("Settings:\n", settings)
    

def main():

    settings = configure()

    start(settings)

if __name__ == '__main__':
    main()