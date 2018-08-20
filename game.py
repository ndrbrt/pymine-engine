from typing import Union, Optional, List
import time
from .board import Board, Cell


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
    
    def uncover_cell(self, row: int, col: int) -> Optional[List[Cell]]:
        cell = self.board.set_cell(row, col, status='uncovered')
        if cell != None:
            if cell.value == 'b':
                self.__loose()
                return
            if cell.value == 0:
                # Uncover neighbors (and nighbors of neighbors with value == 0, etc...)
                uncovered_neighbors = self.__uncover_neighbors(row, col)
                return [cell] + uncovered_neighbors
    
    def __uncover_neighbors(self, row: int, col: int) -> List[Cell]:
        neighbors = self.board.get_neighbors(row, col)
        neighbors_to_uncover = neighbors
        uncovered_neighbors = []
        c = 0
        while len(neighbors_to_uncover) > 0:
            # print(f'iteration {c}: {len(neighbors_to_uncover)}')
            n = neighbors_to_uncover.pop(0)
            n = self.board.set_cell(n.row, n.col, status='uncovered')
            uncovered_neighbors.append(n)
            if n.value == 0:
                for i in self.board.get_neighbors(n.row, n.col):
                    if not i.is_in_list(neighbors_to_uncover) and not i.is_in_list(uncovered_neighbors):
                        neighbors_to_uncover.append(i)
            c += 1
        return uncovered_neighbors
    
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
