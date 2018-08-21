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
        board = []
        for row in range(len(self.board.board)):
            prow = []
            for col in range(len(self.board.board[row])):
                cell = self.board.get_cell(row, col)
                if cell.status == Status.COVERED:
                    prow.append('-')
                else:
                    prow.append(cell.value)
            board.append(prow)
        return str(board)

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
    
    def uncover_cell(self, row: int, col: int) -> Optional[Union[Cell, List[Cell]]]:
        # if self.board.get_cell(row, col).status == Status.UNCOVERED:
        #     return
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
            return cell
    
    def __uncover_neighbors(self, row: int, col: int) -> List[Cell]:
        neighbors = self.board.get_neighbors(row, col)
        neighbors_to_uncover = neighbors
        uncovered_neighbors = []
        # c = 0
        while len(neighbors_to_uncover) > 0:
            # print(f'iteration {c}: {len(neighbors_to_uncover)}')
            n = neighbors_to_uncover.pop(0)
            # if n.status == Status.UNCOVERED:
            #     break
            n = self.board.set_cell(n.row, n.col, status=Status.UNCOVERED)
            uncovered_neighbors.append(n)
            if n.value == 0:
                for i in self.board.get_neighbors(n.row, n.col):
                    if not i.is_in_list(neighbors_to_uncover) and not i.is_in_list(uncovered_neighbors):
                        neighbors_to_uncover.append(i)
            # c += 1
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
