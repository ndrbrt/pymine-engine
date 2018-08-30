import unittest
from pymine.board import Board


class TestCompileMethod(unittest.TestCase):
    def setUp(self):
        self.board = Board(9,9,10)
        self.board.compile()
    
    def test_cells_to_have_a_number_of_bomb_neighbors_equals_to_their_own_value(self):
        for row in range(len(self.board.board)):
            for col in range(len(self.board.board[row])):
                cell = self.board.get_cell(row, col)
                # excluding bomb cells: they can not have a number of bomb neighbors == 'b'
                if cell.value != 'b':
                    with self.subTest():
                        neighbors = self.board.get_neighbors(row, col)
                        bomb_neighbors = [cell for cell in neighbors if cell.value == 'b']
                        self.assertEqual(cell.value, len(bomb_neighbors))


if __name__ == '__main__':
    unittest.main()
