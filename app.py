from typing import Union, Optional, List
import random
import time


class Board():
    def __init__(self, rows: int, cols: int, number_of_bombs: int) -> None:
        self.number_of_cells = rows * cols
        self.rows = rows
        self.cols = cols
        self.board = ['s' for i in range(self.number_of_cells)]
        self.board += ['b' for i in range(number_of_bombs)]
        random.shuffle(self.board)
        self.__as_matrix()
    
    def __str__(self):
        return str(self.board)
    
    def __as_matrix(self):
        matrix = []
        i = 0
        while i < self.number_of_cells:
            matrix.append(self.board[i:i+self.cols])
            i += self.cols
        self.board = matrix
    
    def get_cell(self, row: int, col: int) -> Optional[Union[int, str]]:
        res = None
        f = lambda val: val if val >= 0 else None
        try:
            res = self.board[f(row)][f(col)]
        finally:
            return res
    
    def set_cell(self, row: int, col: int, val: Union[int, str]) -> Optional[Union[int, str]]:
        res = None
        f = lambda val: val if val >= 0 else None
        try:
            self.board[f(row)][f(col)] = val
            res = val
        finally:
            return res
    
    def get_neighbors(self, row: int, col: int) -> List[Union[int, str]]:
        res = []
        res.append(self.get_cell(row - 1, col -1))
        res.append(self.get_cell(row - 1, col))
        res.append(self.get_cell(row - 1, col + 1))
        res.append(self.get_cell(row, col - 1))
        res.append(self.get_cell(row, col + 1))
        res.append(self.get_cell(row + 1, col - 1))
        res.append(self.get_cell(row + 1, col))
        res.append(self.get_cell(row + 1, col + 1))
        return [i for i in res if i != None]
    
    def compile(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                bombs_around = len([i for i in self.get_neighbors(row, col) if i == 'b'])
                if self.get_cell(row, col) != 'b':
                    self.set_cell(row, col, bombs_around)


class Game():
    @staticmethod
    def start(row: int, col: int) -> Board:
        while True:  # Avoid losing the game before it even starts
            board = Board(16, 16, 40)
            if board.get_cell(row, col) != 'b':
                break
        board.compile()
        # self.start_time = time.time()
        # board.uncover_cell(row, col)
        return board


if __name__ == '__main__':
    Game.start(1, 1)
