from typing import Union, Optional, List
import time
from .board import Board, Cell, Status
from enum import Enum


class Outcome(Enum):
    WIN = 1
    LOST = 2


class Game():
    def __init__(self, rows: int, cols: int, number_of_bombs: int) -> None:
        self.rows = rows
        self.cols = cols
        self.number_of_bombs = number_of_bombs
        self.moves = []
        self.uncovered_cells = []
        self.is_over = False
        self.outcome = None

    def __str__(self):
        res = ''
        for row in self.board.board:
            for cell in row:
                if cell.status == Status.COVERED:
                    res += '[ ]'
                elif cell.status == Status.MARKED_BOMB:
                    res += '[f]'
                elif cell.status == Status.MARKED_DOUBT:
                    res += '[?]'
                else:
                    res += f'[{cell.value}]'
            res += '\n'
        return res[:-1]  # skip the last \n

    def start(self, row: int, col: int):
        while True:  # Avoid losing the game before it even starts
            board = Board(self.rows, self.cols, self.number_of_bombs)
            # TODO start with a zero cell
            if board.get_cell(row, col).value != 'b':
                break
        self.board = board
        self.board.compile()
        self.start_time = time.time()
        self.uncover_cell(row, col)
    
    def uncover_cell(self, row: int, col: int) -> Optional[Union[List[Cell]]]:
        '''
        Uncover a given cell if it's not uncovered already.
        If given cell's value is 0, then it also uncovers the neighbors
        of the given cell, and the neighbors of the neighbors recursively.

        Return a list with all the cells uncovered.
        '''
        if self.board.get_cell(row, col).status == Status.UNCOVERED:
            return
        cell = self.board.set_cell(row, col, status=Status.UNCOVERED)
        if cell != None:
            # if cell.value == 'b':  # no more needed, since __is_lost method is implemented - TODO consider if using __is_lost or keep using this
            #     self.__loose()
            #     return
            if cell.value == 0:
                # Uncover neighbors (and nighbors of neighbors with value == 0, etc...)
                uncovered_neighbors = self.__uncover_neighbors(row, col)
                cells = [cell] + uncovered_neighbors
                self.uncovered_cells += cells
                return cells
            self.uncovered_cells.append(cell)
            return [cell]
    
    # TODO: it works but could be written better
    def __uncover_neighbors(self, row: int, col: int) -> List[Cell]:
        '''
        Uncover neighbors recursively.

        Returns a list of uncovered neighbors
        '''
        neighbors = self.board.get_neighbors(row, col)
        neighbors_to_uncover = [n for n in neighbors if n != 'b']
        uncovered_neighbors = []

        while len(neighbors_to_uncover) > 0:
            n = neighbors_to_uncover.pop(0)

            if n.status != Status.UNCOVERED:
                n = self.board.set_cell(n.row, n.col, status=Status.UNCOVERED)
                uncovered_neighbors.append(n)
                if n.value == 0:
                    new_neighbors_to_uncover = [n for n in self.board.get_neighbors(n.row, n.col) if n != 'b']
                    for i in new_neighbors_to_uncover:
                        if not i.is_in_list(neighbors_to_uncover) and not i.is_in_list(uncovered_neighbors):
                            neighbors_to_uncover.append(i)
        return uncovered_neighbors
    
    def mark_cell_as_bomb(self, row: int, col: int) -> Optional[Cell]:
        cell = self.board.get_cell(row, col)
        if cell != None and cell.status != Status.UNCOVERED:
            cell = self.board.set_cell(row, col, status=Status.MARKED_BOMB)
        return cell

    def mark_cell_as_doubt(self, row: int, col: int) -> Optional[Cell]:
        cell = self.board.get_cell(row, col)
        if cell != None and cell.status != Status.UNCOVERED:
            cell = self.board.set_cell(row, col, status=Status.MARKED_DOUBT)
        return cell
    
    def mark_cell_as(self, row: int, col: int, value: str) -> Optional[Cell]:
        pass  # TODO
    
    def unmark_cell(self, row: int, col: int) -> Optional[Cell]:
        cell = self.board.get_cell(row, col)
        if cell != None and cell.status == Status.UNCOVERED:
            cell = self.board.set_cell(row, col, status=Status.COVERED)
        return cell
    
    def check(self) -> Optional[Outcome]:
        if self.__is_lost():
            self.__loose()
            return Outcome.LOST
        elif self.__is_win():
            self.__win()
            return Outcome.WIN
    
    def __is_lost(self):
        uncovered_cells_values = [cell.value for cell in self.uncovered_cells]
        return 'b' in uncovered_cells_values

    def __is_win(self):
        '''
        This method must be called only by self.check(),
        that checks first if the game is not lost.
        That is because in self.uncovered_cells there could be cells with
        value == 'b' (so they are bombs). In such a scenario, this method
        could return True even though the game is actually lost.
        '''
        return len(self.uncovered_cells) == self.board.number_of_cells - self.board.number_of_bombs
    
    def __win(self):
        self.__end(Outcome.WIN)
    
    def __loose(self):
        self.__end(Outcome.LOST)
    
    def __end(self, outcome: Outcome):
        self.end_time = time.time()
        self.outcome = outcome
        self.is_over = True
