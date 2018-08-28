from typing import Union, Optional, List
import time
from .board import Board, Cell, Status


class Game():
    def __init__(self, rows: int, cols: int, number_of_bombs: int) -> None:
        self.rows = rows
        self.cols = cols
        self.number_of_bombs = number_of_bombs
        self.moves = []
        self.uncovered_cells = []

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
            if cell.value == 'b':
                self.__loose()
                return
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
        if cell != None and cell.status != Status.UNCOVERED:
            cell = self.board.set_cell(row, col, status=Status.COVERED)
        return cell
    
    def __check(self):
        pass
    
    def __is_win(self):
        return len(self.uncovered_cells) == self.board.number_of_cells - self.board.number_of_bombs
    
    def __win(self):
        return False
    
    def __loose(self):
        return False
    
    def __end(self, outcome: str):
        self.end_time = time.time()
        if outcome == 'win':
            pass
        elif outcome == 'lost':
            pass
