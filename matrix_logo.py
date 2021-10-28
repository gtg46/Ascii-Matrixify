import json
from json.decoder import JSONDecodeError
from typing import Callable, NoReturn
import argparse
from random import Random
from ascii_art import Ascii_art
from matrixify import Matrixify
import re

'''
Author: Grant Garcelon
Date: October 2021
'''

DESCRIPTION = "description"
SETTINGS = "settings"
FLAGS = "flags"
SETUP_PATH = "config/setup.json"
CONFIG = "config"
IMG_PATH = "img_path"
CONTRAST = "contrast"
BRIGHTNESS = "brightness"
ASCII_RAMP = "ascii_ramp"
OUT_RES = "out_res"
HEIGHT_ASJUST = "height_adjust"
INVERT = "invert"
SEED = "seed"
STREAK_SPACING = "streak_spacing"
STREAK_LENGTH = "streak_length"
STREAK_MIN = "streak_min"
MATRIX = "matrix"
COLOR = "color"
SPACE = " "
EMPTY = ""
READ = "r"
WRITE = "w"
NEW_LINE = "\n"
OUTPUT = "output"
TERMINAL = "terminal"
IMAGE = "image"
TEXT = "text"

ASCII_MIN = 32
ASCII_MAX = 128


def get_json(path: str) -> dict:
    '''Reads a json file at the specified path
    and returns the python objects
    '''

    loaded = None
    json_file = None

    try:
        json_file = open(path , READ)
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
    parser = argparse.ArgumentParser(defaults[DESCRIPTION])
    for setting in defaults[SETTINGS]:
        flags = setting.pop(FLAGS).split()
        parser.add_argument(
            *flags,
            **setting
        )

    return vars(parser.parse_args())

def list_to_str(ascii_art: list, size: int) -> str:
    ret_str = EMPTY
    for i, ascii_val in enumerate(ascii_art):
        if not i % size:
            ret_str += NEW_LINE
        ret_str += ascii_val
    return ret_str

def configure() -> dict:
    
    setup = get_json(SETUP_PATH)
    settings = parse_args(setup)

    if settings[CONFIG] != None:
        config = get_json(settings[CONFIG])

        if config != None:
            settings.update(config)
        else:
            print("Using default settings")

    return settings

def start(settings: dict) -> NoReturn:
    if settings[IMG_PATH] != None: # ascii art object
        ascii_art = Ascii_art(
            settings[IMG_PATH],
            float(settings[CONTRAST]),
            float(settings[BRIGHTNESS]),
            settings[ASCII_RAMP],
            int(settings[OUT_RES]),
            float(settings[HEIGHT_ASJUST]),
            settings[INVERT]
        )
        ascii_list = [val for val in ascii_art.next_ascii(settings[COLOR])]

    else: # Generates an array of random ascii characters
        size = int(settings[OUT_RES]) * int(settings[OUT_RES])
        r = Random(settings[SEED])
        ascii_list = list()
        for i in range(size):
            ascii_list.append(chr(r.randrange(ASCII_MIN, ASCII_MAX)))

    if settings[MATRIX]:
        matrix = Matrixify(
            len(ascii_list),
            int(settings[OUT_RES]),
            int(settings[STREAK_SPACING]),
            int(settings[STREAK_LENGTH]),
            int(settings[STREAK_MIN]),
            settings[SEED]
        )
        
        ascii_out = [ascii_val if matrix_val else SPACE for ascii_val, matrix_val in zip(ascii_list , matrix.next_in_col())]
    else:
        ascii_out = ascii_list

    if settings[OUTPUT] == TERMINAL:
        print(list_to_str(ascii_out, int(settings[OUT_RES])))
    elif settings[OUTPUT] == IMAGE:
        pass # not implemented
    elif settings[OUTPUT] == TEXT:
        prompt = "Please enter the new filename"
        example = " e.g. \"new_out_file.txt\""
        cursor = " >> "
        folder = "files/"
        filename = input(prompt + cursor)
        while not re.fullmatch("[^/\\. ]+.txt", filename):
            filename = input(prompt + example + cursor)
        try:
            file = open(folder + filename, WRITE)
        except Exception as e:
            print("File Error")
            print(e)
        if file != None:
            file.write(list_to_str(ascii_out, int(settings[OUT_RES])))
            file.close()
    else:
        print("Inavlid output type")


def main():
    settings = configure()
    start(settings)

if __name__ == '__main__':
    main()