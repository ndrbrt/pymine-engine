from typing import Union, Optional, List
import random
from enum import Enum


class Status(Enum):
    COVERED = 1
    UNCOVERED = 2
    MARKED_BOMB = 3
    MARKED_DOUBT = 4


class Cell():
    def __init__(self, value: Optional[Union[int, str]] = None, status: Status = Status.COVERED) -> None:
        self.value = value
        self.status = status
        self.row = None
        self.col = None
    
    def __str__(self):
        return f'<Cell: {self.value} {self.status.name.lower()}>'
    
    def is_in_list(self, ls: List) -> bool:
        for i in ls:
            if i.row == self.row and i.col == self.col:
                return True
        return False


class Board():
    def __init__(self, rows: int, cols: int, number_of_bombs: int) -> None:
        self.number_of_cells = rows * cols
        self.number_of_bombs = number_of_bombs
        self.number_of_safe_cells = self.number_of_cells - number_of_bombs
        self.rows = rows
        self.cols = cols
        self.board = [Cell('s') for i in range(self.number_of_safe_cells)]
        self.board += [Cell('b') for i in range(number_of_bombs)]
        random.shuffle(self.board)
        self.__as_matrix()
    
    def __str__(self):
        res = ''
        for row in self.board:
            for cell in row:
                res += f'[{cell.value}]'
            res += '\n'
        return res[:-1]  # skip the last \n
    
    def __as_matrix(self):
        matrix = []
        i = 0
        while i < self.number_of_cells:
            matrix.append(self.board[i:i+self.cols])
            i += self.cols
        self.board = matrix
    
    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        res = None
        f = lambda x: x if x >= 0 else None
        try:
            res = self.board[f(row)][f(col)]
        finally:
            return res
    
    def set_cell(self, row: int, col: int,
        value: Optional[Union[int, str]] = None,
        status: Optional[Status] = None) -> Optional[Cell]:
        res = None
        f = lambda x: x if x >= 0 else None
        try:
            cell = self.board[f(row)][f(col)]
            if value != None: cell.value = value
            if status != None: cell.status = status
            res = cell
        finally:
            return res
    
    def get_neighbors(self, row: int, col: int) -> List[Cell]:
        res = []
        neighbors = [
            (row - 1, col -1), (row - 1, col), (row - 1, col + 1),
            (row, col - 1), (row, col + 1),
            (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
        for n in neighbors:
            cell = self.get_cell(n[0], n[1])
            if cell != None:
                cell.row, cell.col = n[0], n[1]
                res.append(cell)
        return res
    
    def compile(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                bombs_around = len([i for i in self.get_neighbors(row, col) if i.value == 'b'])
                if self.get_cell(row, col).value != 'b':
                    self.set_cell(row, col, bombs_around)
