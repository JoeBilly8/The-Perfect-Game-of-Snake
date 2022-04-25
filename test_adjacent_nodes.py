import unittest
from snake_ai_functions.find_adjacent_nodes import find_adjacent_nodes


# The assertCountEqual is a misleading test name - it is infact checking the contents of the lists are the same
# but we are using this as opposed to assertItemsEqual because we don't care about the order.
class TestAdjacentNodes(unittest.TestCase):
    # Use a 3x3 grid to check all 9 possible cases without a snake body
    def test_find_adjacent_nodes(self):
        grid_rows = 3
        grid_columns = 3
        # Top left corner adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [0, 0], grid_rows, grid_columns, []), [[0, 1], [1, 0]])

        # Top middle adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [1, 0], grid_rows, grid_columns, []), [[0, 0], [1, 1], [2, 0]])

        # Top right corner adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [2, 0], grid_rows, grid_columns, []), [[2, 1], [1, 0]])

        # Right edge side adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [2, 1], grid_rows, grid_columns, []), [[2, 0], [1, 1], [2, 2]])

        # Bottom right corner adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [2, 2], grid_rows, grid_columns, []), [[2, 1], [1, 2]])

        # Bottom middle adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [1, 2], grid_rows, grid_columns, []), [[2, 2], [1, 1], [0, 2]])

        # Bottom left corner adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [0, 2], grid_rows, grid_columns, []), [[1, 2], [0, 1]])

        # Left edge side adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [0, 1], grid_rows, grid_columns, []), [[0, 0], [1, 1], [0, 2]])

        # Middle of the grid adjacent nodes
        self.assertCountEqual(find_adjacent_nodes(
            [1, 1], grid_rows, grid_columns, []), [[0, 1], [1, 0], [2, 1], [1, 2]])


if __name__ == '__main__':
    unittest.main()
