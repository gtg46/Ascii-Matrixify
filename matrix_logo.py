import json
from json.decoder import JSONDecodeError
from typing import Callable, NoReturn, Tuple
import argparse
from random import Random
from ascii_art import Ascii_art
from matrixify import Matrixify
import re
from PIL import Image, ImageDraw, ImageFont

'''
Author: Grant Garcelon
Date: October 2021
'''

DESCRIPTION = "description"
SETTINGS = "settings"
FLAGS = "flags"
SETUP_PATH = "configs/setup.json"
CONFIG = "config"
IMG_PATH = "img_path"
BACK_COL = "back_col"
TEXT_COL = "text_col"
TITLE_COL = "title_col"
TITLE_POS = "title_pos"
TITLE_TEXT = "title_text"
TITLE_SIZE = "title_size"
TITLE_FONT = "title_font"
TEXT_FONT = "text_font"
CHAR_OFFSET = "char_offset"
CONTRAST = "contrast"
BRIGHTNESS = "brightness"
ASCII_RAMP = "ascii_ramp"
SIZE = "size"
HEIGHT_ASJUST = "height_adjust"
INVERT = "invert"
SEED = "seed"
STREAK_SPACING = "streak_spacing"
STREAK_LENGTH = "streak_length"
STREAK_MIN = "streak_min"
MATRIX = "matrix"
COLOR = "color"
TRANSPARENT = "transparent"
MATRIX_DIR = "matrix_dir"
HORIZONTAL = "horizontal"
VERTICAL = "vertical"
FILENAME = "filename"
OUTPUT_FOLDER = "output_folder"

SPACE = " "
EMPTY = ""
READ = "r"
WRITE = "w"
NEW_LINE = "\n"
OUTPUT = "output"
TERMINAL = "terminal"
IMAGE = "image"
TEXT = "text"
PNG = ".png"
TXT = ".txt"

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
            # Overrides command line args with config file values.
            settings.update(config)

    return settings

def get_new_filename(extention: str) -> str:
    prompt = "Please enter the new filename"
    example = " e.g. \"newfile" + extention + "\""
    cursor = " >> "
    filename = input(prompt + cursor)
    while not check_filename(filename, extention):
        filename = input(prompt + example + cursor)
    return filename

def check_filename(filename: str, extention: str) -> bool:
    return re.fullmatch("[^/\\. ]+" + extention, filename)

def text_color_arr(settings:dict, size: int) -> list:
    color_list = list()
    for i in range(size):
        color_list.append(eval(settings[TEXT_COL]))
    return color_list

def get_xy(length: int, size: int, char_size: Tuple[int, int]) -> Tuple[int, int]:
    X = 0
    Y = 1
    j = -1 
    for i in range(length):
        x = i % size
        if not x:
            j += 1
        yield (x * char_size[X], j * char_size[Y])

def get_out_size(length: int, size: int, char_size: Tuple[int, int]) -> Tuple[int, int]:
    X = 0
    Y = 1
    vert_size = int(length / size)
    return (size * char_size[X], vert_size * char_size[Y])


def start(settings: dict) -> NoReturn:
    
    if settings[IMG_PATH] != None: # ascii art object
        ascii_art = Ascii_art(
            settings[IMG_PATH],
            float(settings[CONTRAST]),
            float(settings[BRIGHTNESS]),
            settings[ASCII_RAMP],
            int(settings[SIZE]),
            float(settings[HEIGHT_ASJUST]),
            settings[INVERT]
        )
        size = ascii_art.get_orig_size()
        color = settings[COLOR] and settings[OUTPUT] == TERMINAL
        ascii_list = [val for val in ascii_art.next_ascii(color)]
        color = ascii_art.get_colors() if settings[COLOR] else text_color_arr(settings, len(ascii_list))

    else: # Generates an array of random ascii characters
        size = int(settings[SIZE]) * int(settings[SIZE])
        r = Random(settings[SEED])
        ascii_list = list()
        for i in range(size):
            ascii_list.append(chr(r.randrange(ASCII_MIN, ASCII_MAX)))
        color = text_color_arr(settings, len(ascii_list))
            

    if settings[MATRIX]:
        matrix = Matrixify(
            len(ascii_list),
            int(settings[SIZE]),
            int(settings[STREAK_SPACING]),
            int(settings[STREAK_LENGTH]),
            int(settings[STREAK_MIN]),
            settings[SEED]
        )
        if settings[MATRIX_DIR] == VERTICAL:
            ascii_out = [ascii_val if matrix_val else SPACE for ascii_val, matrix_val in zip(ascii_list , matrix.next_in_col())]
        elif settings[MATRIX_DIR] == HORIZONTAL:
            ascii_out = [ascii_val if matrix_val else SPACE for ascii_val, matrix_val in zip(ascii_list , matrix.next_in_row())]
        else:
            raise Exception("unknown matrix direction") 
    else:
        ascii_out = ascii_list

    folder = settings[OUTPUT_FOLDER]
    if settings[OUTPUT] == TERMINAL:
        print(list_to_str(ascii_out, int(settings[SIZE])))

    elif settings[OUTPUT] == IMAGE:
        out_img = Image.new('RGB', get_out_size(len(ascii_out), int(settings[SIZE]), eval(settings[CHAR_OFFSET])), eval(settings[BACK_COL]))
        drawer = ImageDraw.Draw(out_img)

        for xy, char, fill in zip(get_xy(len(ascii_out), int(settings[SIZE]), eval(settings[CHAR_OFFSET])), ascii_out, color):
            drawer.text(xy, char, fill)

        if settings[TITLE_TEXT] != None:
            if settings[TITLE_FONT] != None:
                title_font = ImageFont.truetype(settings[TITLE_FONT], size=int(settings[TITLE_SIZE]))
            else:
                title_font = ImageFont.load_default()           
            drawer.multiline_text(
                eval(settings[TITLE_POS]),
                settings[TITLE_TEXT],
                fill=eval(settings[TITLE_COL]),
                font=title_font
            )
        
        if settings[FILENAME] != None and check_filename(settings[FILENAME], PNG):
            path = folder + settings[FILENAME]
        else:
            path = folder + get_new_filename(PNG)
        out_img.save(path)
        print("File \"" + path + "\"created")

    elif settings[OUTPUT] == TEXT:
        if settings[FILENAME] != None and check_filename(settings[FILENAME], TXT):
            path = folder + settings[FILENAME]
        else:
            path = folder + get_new_filename(TXT)

        try:
            file = open(path, WRITE)
            print("File \"" + path + "\"created")
        except Exception as e:
            print("File Error")
            print(e)
        if file != None:
            file.write(list_to_str(ascii_out, int(settings[SIZE])))
            file.close()

    else:
        print("Inavlid output type")


def main():
    settings = configure()
    print("Configured, generating...")
    start(settings)
    print("Done.")

if __name__ == '__main__':
    main()