import unittest
from pymine.board import Board

class TestNeighborsNumber(unittest.TestCase):
    def setUp(self):
        self.board = Board(9,9,10)

    # first cell
    def test_cell_0_0_to_have_3_neighbors(self):
        neighbors = self.board.get_neighbors(0,0)
        self.assertEqual(len(neighbors), 3)

    # cell on the top edge
    def test_cell_0_1_to_have_5_neighbors(self):
        neighbors = self.board.get_neighbors(0,1)
        self.assertEqual(len(neighbors), 5)

    # cell on the left edge
    def test_cell_1_0_to_have_5_neighbors(self):
        neighbors = self.board.get_neighbors(1,0)
        self.assertEqual(len(neighbors), 5)

    # cell on the right edge
    def test_cell_7_8_to_have_5_neighbors(self):
        neighbors = self.board.get_neighbors(7,8)
        self.assertEqual(len(neighbors), 5)

    # cell on the bottom edge
    def test_cell_8_7_to_have_5_neighbors(self):
        neighbors = self.board.get_neighbors(8,7)
        self.assertEqual(len(neighbors), 5)

    # last cell
    def test_cell_8_8_to_have_3_neighbors(self):
        neighbors = self.board.get_neighbors(8,8)
        self.assertEqual(len(neighbors), 3)

    # a cell in the middle of the board
    def test_cell_5_5_to_have_8_neighbors(self):
        neighbors = self.board.get_neighbors(5,5)
        self.assertEqual(len(neighbors), 8)

    # a cell that does not exists on the board
    def test_cell_10_10_to_have_0_neighbors(self):
        neighbors = self.board.get_neighbors(10,10)
        self.assertEqual(len(neighbors), 0)
    

if __name__ == '__main__':
    unittest.main()
