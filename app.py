from typing import Union, Optional, List
import random
import time


class Cell():
    def __init__(self, value: Optional[Union[int, str]] = None, status: str = 'covered') -> None:
        self.value = value
        self.status = status
        self.row = None
        self.col = None
    
    def __str__(self):
        return f'<Cell: {self.value} {self.status}>'
    
    def is_in_list(self, ls: List) -> bool:
        for i in ls:
            if i.row == self.row and i.col == self.col:
                return True
        return False


class Board():
    def __init__(self, rows: int, cols: int, number_of_bombs: int) -> None:
        self.number_of_cells = rows * cols
        self.rows = rows
        self.cols = cols
        self.board = [Cell('s') for i in range(self.number_of_cells)]
        self.board += [Cell('b') for i in range(number_of_bombs)]
        random.shuffle(self.board)
        self.__as_matrix()
    
    def __str__(self):
        board = []
        for row in self.board:
            board.append([cell.value for cell in row])
        return str(board)
    
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
        status: Optional[Union[int, str]] = None) -> Optional[Cell]:
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
    
    @staticmethod
    def append_unique_neighbor(neighbor: Cell, list_of_neighbors: List[Cell]) -> None:
        '''Append a neighbor cell to a list only if it's not already in that list'''
        for i in list(list_of_neighbors):
            if i.row == neighbor.row and i.col == neighbor.col:
                return
        list_of_neighbors.append(neighbor)
    
    def compile(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                bombs_around = len([i for i in self.get_neighbors(row, col) if i.value == 'b'])
                if self.get_cell(row, col).value != 'b':
                    self.set_cell(row, col, bombs_around)


class Game():
    moves = []

    def __str__(self):
        board = []
        for row in range(len(self.board.board)):
            prow = []
            for col in range(len(self.board.board[row])):
                cell = self.board.get_cell(row, col)
                if cell.status == 'covered':
                    prow.append('-')
                else:
                    prow.append(cell.value)
            board.append(prow)
        return str(board)

    def start(self, row: int, col: int):
        while True:  # Avoid losing the game before it even starts
            board = Board(16, 16, 40)
            if board.get_cell(row, col).value != 'b':
            # if board.get_cell(row, col).value == 0:
                break
        self.board = board
        self.board.compile()
        self.start_time = time.time()
        self.uncover_cell(row, col)
    
    def uncover_cell(self, row: int, col: int):
        cell = self.board.set_cell(row, col, status='uncovered')
        if cell != None:
            if cell.value == 'b':
                self.__loose()
                return
            if cell.value == 0:
                # Uncover neighbors (and nighbors of neighbors etc...)
                neighbors = self.board.get_neighbors(row, col)
                neighbors_to_uncover = neighbors
                uncovered_neighbors = []
                c = 0
                while len(neighbors_to_uncover) > 0:
                    print(f'iteration {c}: {len(neighbors_to_uncover)}')
                    n = neighbors_to_uncover.pop(0)
                    n = self.board.set_cell(n.row, n.col, status='uncovered')
                    uncovered_neighbors.append(n)
                    if n.value == 0:
                        for i in self.board.get_neighbors(n.row, n.col):
                            if not i.is_in_list(neighbors_to_uncover) and not i.is_in_list(uncovered_neighbors):
                                neighbors_to_uncover.append(i)
                    c += 1
    
    def mark_cell_as_bomb(self, row: int, col: int):
        pass

    def mark_cell_as_doubt(self):
        pass
    
    def unmark_cell(self):
        pass
    
    def __check(self):
        pass
    
    def __win(self):
        return False
    
    def __loose(self):
        return False


if __name__ == '__main__':
    game = Game()
