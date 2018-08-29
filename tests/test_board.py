import unittest
from pymine.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(9,9,10)
    
    def test_board_to_have_10_bombs(self):
        number_of_bombs = 0
        for row in self.board.board:
            row = ['b' for cell in row if cell.value == 'b']
            number_of_bombs += len(row)
        self.assertEqual(number_of_bombs, 10)
    
    def test_board_to_have_71_safe_cells(self):
        number_of_bombs = 0
        for row in self.board.board:
            row = ['s' for cell in row if cell.value == 's']
            number_of_bombs += len(row)
        self.assertEqual(number_of_bombs, 71)
    

if __name__ == '__main__':
    unittest.main()
