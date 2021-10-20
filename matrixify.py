import random 

class Matrixify():
    def __init__(
        self,
        size: int,
        density: float,
        ascii_ramp: str = None,
        chars: str = None,
        colors: list = None, 
        seed = None
    ):

        self.size = size
        self.density = density
        self.ascii_ramp = ascii_ramp
        self.chars = chars
        self.colors = colors
        self.random = random.Random(seed)
        
        if self.chars != None:
            self.matrix = self.initialize()
        else:
            self.matrix = self.init_random()

    def init_random(self) -> list:
        '''Initializes a square list to random characters
        
        These lists are indexed column, row
        '''
        bound = len(self.ascii_ramp)
        matrix = list()
        for i in range(self.size):
            column = list()
            for j in range(self.size):
                char = self.ascii_ramp[self.random.randrange(bound)]
                column.append(char)
            matrix.append(column)
        return matrix

    def initialize(self) -> list:
        matrix = list()
        
        img_height = int(len(self.chars) / self.size)
        for i in range(self.size):
            column = list()
            for j in range(img_height):
                index = (j * self.size) + i
                char = self.chars[index]
                
                column.append(char)
            matrix.append(column)
        return matrix



    def __str__(self):
        img_height = int(len(self.chars) / self.size)
        ret_str = ""
        for i in range(img_height):
            for j in range(self.size):
                ret_str += self.matrix[j][i]
        return ret_str

    def get_matrix(self):
        return self.matrix

    def get_chars(self):
        return self.chars

    def color_str(self):
        img_height = int(len(self.chars) / self.size)
        ret_str = ""
        for i in range(img_height):
            for j in range(self.size):
                ret_str += self.get_ansi(self.colors[(i * self.size) + j])
                ret_str += self.matrix[j][i]
        return ret_str



