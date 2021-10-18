import json
from json.decoder import JSONDecodeError
import sys
from typing import Callable, NoReturn
import argparse
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

def parse_args():
    parser = argparse.ArgumentParser("Creates a Matrix style effect for making logos.")
    parser.add_argument('-c', '--config' , help="path to a json config file", default="config/default_settings.json")
    parser.add_argument('-s', '-seed', help="this seed overrides the config file")
    return parser.parse_args()

def get_json(path: str) -> dict:

    loaded = None

    try:
        json_file = open(path , 'r')
        loaded = json.load(json_file)

    except JSONDecodeError as e:
        print(path, "- Invalid JSON")

    except FileNotFoundError as e:
        print(path, "-",  e.strerror)
        
    finally:
        json_file.close()

    return loaded




def configure(args: dict) -> dict:
    DEFAULTS_PATH = "config/default_settings.json"
    settings = get_json(DEFAULTS_PATH)

    if settings != None:
        if args["config"] != DEFAULTS_PATH:
            user_settings = get_json(args["config"])

            if user_settings != None:
                settings.update(user_settings)

        settings.update(args)

    return settings

def start(settings: dict) -> NoReturn:
    pass
    

def main():
    args = vars(parse_args())

    settings = configure(args)

    start(settings)

if __name__ == '__main__':
    main()