from operator import ge
import string
import unittest
import random
from snake_ai_functions.prim_maze import maze


class TestPrimMaze(unittest.TestCase):

    # Instantiate 3x3 test maze to test on
    test_maze = maze(3, 3)

    # Use a 3x3 grid to check all 9 possible cases of adjacent neighbours
    def test_get_cell_neighbours(self):
        # Top left corner adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((0, 0)), [(0, 1), (1, 0)])

        # Top middle adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((1, 0)), [(0, 0), (1, 1), (2, 0)])

        # Top right corner adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((2, 0)), [(2, 1), (1, 0)])

        # Right edge side adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((2, 1)), [(2, 0), (1, 1), (2, 2)])

        # Bottom right corner adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((2, 2)), [(2, 1), (1, 2)])

        # Bottom middle adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((1, 2)), [(2, 2), (1, 1), (0, 2)])

        # Bottom left corner adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((0, 2)), [(1, 2), (0, 1)])

        # Left edge side adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((0, 1)), [(0, 0), (1, 1), (0, 2)])

        # Middle of the grid adjacent nodes
        self.assertCountEqual(
            self.test_maze.get_cell_neighbours((1, 1)), [(0, 1), (1, 0), (2, 1), (1, 2)])

    # Testing: produces the correct types of return values ie list of cell and wall in wall out
    # Checking that the values are within the expected range
    def test_generate_prim_maze(self):
        generated_maze = self.test_maze.generate_prim_maze()
        print(generated_maze)

        # Ensure length of maze is correct
        self.assertEqual(len(generated_maze), 9)

        # Ensure the data type of the generated maze is correct
        self.assertTrue(type(generated_maze) is list)

        # Ensure the data type for the cells in the path is correct (use randint for better coverage)
        self.assertTrue(type(generated_maze[random.randint(0, 8)][0]), tuple)

        # Ensure the data type for the wall info is correct
        self.assertTrue(type(generated_maze[random.randint(0, 8)][1]), string)


if __name__ == '__main__':
    unittest.main()
