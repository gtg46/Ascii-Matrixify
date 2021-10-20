import json
from json.decoder import JSONDecodeError
from typing import Callable, NoReturn
import argparse

from ascii_art import ascii_art
from matrixify import Matrixify

magenta ="\x1b[38;5;57m"
cat_purp = "\x1b[38;2;73;47;146m"

def get_color_printer(r: str, g: str, b:str) -> Callable[[str], NoReturn]:
    '''This method returns a function that prints in color

    This method is no longer used in this file.
    
    '''
    ANSI_color = "\x1b[38;2;"
    ANSI_color += r + ";" + g + ";" + b + "m"
    def color_printer(value: str, end="\n"):
        print(ANSI_color, value, sep="", end=end)
    return color_printer


def read_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()



def get_json(path: str) -> dict:
    '''Reads a json file at the specified path
    and returns the python objects
    '''

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
        flags = setting.pop("flags").split()
        parser.add_argument(
            *flags,
            **setting
        )

    return vars(parser.parse_args())

def configure() -> dict:
    DEFAULTS_PATH = "config/setup.json"
    setup = get_json(DEFAULTS_PATH)
    settings = parse_args(setup)

    if settings["config"] != None:
        config = get_json(settings["config"])

        if config != None:
            settings.update(config)
        else:
            print("Using default settings")

    return settings

def start(settings: dict) -> NoReturn:
    if settings["img_path"] != None:
        art_maker = ascii_art(
            settings["img_path"],
            float(settings["contrast"]),
            float(settings["brightness"]),
            settings["ascii_ramp"],
            int(settings["out_res"]),
            float(settings["height_multiplier"])
        )

        print(art_maker.__str__(color=settings["color"]))

        
    
    '''matrix = Matrixify(
        int(settings["out_res"]),
        float(settings["density"]),
        settings["ascii_ramp"],
        chars,
        colors,
        settings["seed"]
    )
    print(matrix.color_str())'''
    

    
    

def main():

    settings = configure()

    start(settings)

if __name__ == '__main__':
    main()