from typing import Tuple
from PIL import Image, ImageEnhance

class Ascii_art():
    def __init__(
            self,
            image_path: str, # Path the the image
            contrast: float, # Value to adjust the contrast
            brightness: float, # value to adjust the brightness
            ascii_ramp: str, 
            size: int,
            height_multiplier: float
        ):

        self.image = Image.open(image_path)
        self.image = self.image.convert('RGB') # If the image is something other than rgb this converts it to that.
        self.set_contrast(contrast)
        self.set_brightness(brightness)
        self.ascii_ramp = ascii_ramp
        self.size = size
        self.height_multiplier = height_multiplier
        self.c_pixels = None
        self.bw_pixels = None
        self.generate()

    def set_contrast(self, new_contrast: float):
        self.image = ImageEnhance.Contrast(self.image).enhance(new_contrast)

    def set_brightness(self, new_brightness: float):
        self.image = ImageEnhance.Brightness(self.image).enhance(new_brightness)


    def generate(self):
        self.image_resize()
        self.c_pixels = list(self.image.getdata())
        self.image = self.image.convert('L') # Convert to black and white.
        self.bw_pixels = list(self.image.getdata())
        self.num_pixels = len(self.bw_pixels)

    def __iter__(self):
        return self.next_ascii
    
    def __next__(self):
        return self.pixels()

   
    def image_resize(self):
        '''Resizes the image to the given size'''
        width, height = self.image.size
        ratio = height / width 
        new_size = self.size, int((self.size * ratio) * self.height_multiplier)
        self.image = self.image.resize(new_size)

    def pixels(self) -> Tuple[int, Tuple[int, int, int]]:
        assert(
            len(self.bw_pixels) == len(self.c_pixels)
        )
        
        for i in range(len(self.bw_pixels)):
            pixel = (self.bw_pixels[i], self.c_pixels[i])
            yield pixel

    def __len__(self):
        return self.num_pixels

    def pixel_to_ascii(self, intensity: int) -> str:
        INTENSITY_MAX = 255
        ascii_val = ""
        if 0 <= intensity < INTENSITY_MAX:
            ramp_index = int(intensity / (INTENSITY_MAX / len(self.ascii_ramp)))
            ascii_val = self.ascii_ramp[ramp_index]
        elif intensity == INTENSITY_MAX:
            ascii_val = self.ascii_ramp[-1]
        return ascii_val

    def rgb_to_ansi(self, rgb: Tuple[int, int, int]) -> str:
        ansi_color = "\x1b[38;2;"
        r, g, b = rgb
        ansi_color += str(r) + ";" + str(g) + ";" + str(b) + "m"
        return ansi_color

    def next_ascii(self, color=False) -> str:
        for pixel in self.pixels():
            bw , rgb, = pixel
            pixel_str = ""
            if color:
                pixel_str += self.rgb_to_ansi(rgb)
            pixel_str += self.pixel_to_ascii(bw)
            yield pixel_str





    def __str__(self, color=False):
        ret_str = ""
        for i, pixel in enumerate(self.pixels()):
            bw , rgb, = pixel
            if not i % self.size:
                ret_str += "\n"
            if color:
                ret_str += self.rgb_to_ansi(rgb)
            ret_str += self.pixel_to_ascii(bw)
            
        return ret_str


