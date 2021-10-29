from typing import Tuple
from PIL import Image, ImageEnhance, ImageOps

'''
Author: Grant Garcelon
Date: October 2021
'''

class Ascii_art():
    def __init__(
            self,
            image_path: str, # Path the the image
            contrast: float, # Value to adjust the contrast
            brightness: float, # value to adjust the brightness
            ascii_ramp: str, 
            size: int,
            height_multiplier: float,
            invert = False
        ):

        self.image = Image.open(image_path)
        self.image = self.image.convert('RGB') # If the image is something other than rgb this converts it to that.
        self.orig_size = self.image.size
        self._set_contrast(contrast)
        self._set_brightness(brightness)
        if invert:
            self._invert_image()
        self.ascii_ramp = ascii_ramp
        self.size = size
        self.height_multiplier = height_multiplier
        self.c_pixels = None
        self.bw_pixels = None
        self._generate()

    def _set_contrast(self, new_contrast: float):
        self.image = ImageEnhance.Contrast(self.image).enhance(new_contrast)

    def _set_brightness(self, new_brightness: float):
        self.image = ImageEnhance.Brightness(self.image).enhance(new_brightness)

    def _invert_image(self):
        self.image = ImageOps.invert(self.image)


    def _generate(self):
        self._image_resize()
        self.c_pixels = list(self.image.getdata())
        self.image = self.image.convert('L') # Convert to black and white.
        self.bw_pixels = list(self.image.getdata())
        self.num_pixels = len(self.bw_pixels)

    def get_orig_size(self):
        return self.orig_size

    def _image_resize(self):
        '''Resizes the image to the given size'''
        width, height = self.image.size
        ratio = height / width 
        new_size = self.size, int((self.size * ratio) * self.height_multiplier)
        self.image = self.image.resize(new_size)

    def pixels(self) -> Tuple[int, Tuple[int, int, int]]:
        for bw, c in zip(self.bw_pixels, self.c_pixels):
            yield (bw, c)

    def get_colors(self) -> list:
        return self.c_pixels
          
    def __len__(self):
        return self.num_pixels

    def _pixel_to_ascii(self, intensity: int) -> str:
        INTENSITY_MAX = 255
        ascii_val = ""
        if 0 <= intensity < INTENSITY_MAX:
            ramp_index = int(intensity / (INTENSITY_MAX / len(self.ascii_ramp)))
            ascii_val = self.ascii_ramp[ramp_index]
        elif intensity == INTENSITY_MAX:
            ascii_val = self.ascii_ramp[-1]
        return ascii_val

    def _rgb_to_ansi(self, rgb: Tuple[int, int, int]) -> str:
        ansi_color = "\x1b[38;2;"
        r, g, b = rgb
        ansi_color += str(r) + ";" + str(g) + ";" + str(b) + "m"
        return ansi_color

    def next_ascii(self, color=False) -> str:
        for pixel in self.pixels():
            bw , rgb, = pixel
            pixel_str = ""
            if color:
                pixel_str += self._rgb_to_ansi(rgb)
            pixel_str += self._pixel_to_ascii(bw)
            yield pixel_str

    def __str__(self, color=False):
        ret_str = ""
        for i, pixel in enumerate(self.pixels()):
            bw , rgb, = pixel
            if not i % self.size:
                ret_str += "\n"
            if color:
                ret_str += self._rgb_to_ansi(rgb)
            ret_str += self._pixel_to_ascii(bw)
            
        return ret_str

def tester():
    ascii_art = Ascii_art(
        "files/check.jpg",
        1.0,
        1.0,
        " _-.,:;*$S#@",
        100,
        .45
    )
    for val in ascii_art.next_ascii():
        print(val, sep="", end="")




if __name__ == '__main__':
    tester()


