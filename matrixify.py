import random 

'''
Author: Grant Garcelon
Date: October 2021
'''

class Matrixify():
    def __init__(
            self,
            size : int,
            width: int,
            streak_spacing: int,
            streak_length: int,
            streak_min: int,
            seed = None
        ):

        self.size = size
        self.row_size = width
        self.col_size = int(size / width)
        self.streak_spacing = streak_spacing
        self.streak_length = streak_length
        self.streak_min = streak_min
        self.random = random.Random(seed)
        self.matrix = self._init_matrix()

    def _spacing_calc(self, last: bool) -> int:
        if last: # if the last one was a streak
            spacing = self.streak_spacing # this one will be a space
        else: # if the last one was a space
            spacing = self.streak_length # this one will be a streak
        
        return random.randint(self.streak_min, spacing)

    def _init_matrix(self) -> list:
        matrix = [bool(self.random.randint(0,1))]
        n = self._spacing_calc(matrix[0])
        for i in range(self.size - 1):
            if n > 0:
                matrix.append(matrix[i])
                n -= 1
            else:
                n = self._spacing_calc(matrix[i])
                matrix.append(not matrix[i])
                
        return matrix

    def __str__(self) -> str:
        ret_str = ""
        i = 0
        for val in self.next_in_col():
            if not i % self.row_size:
                ret_str += "\n"
            ret_str += "1" if val else "0"
            i += 1
        return ret_str

    def next_in_col(self):
        for i in range(self.col_size):
            for j in range(self.row_size):
                yield self.matrix[(j * self.col_size) + i]

    def next_in_row(self):
        for value in self.matrix:
            yield value

