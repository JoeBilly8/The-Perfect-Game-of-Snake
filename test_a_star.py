import unittest
from snake_ai_functions.a_star_search import a_star_path


class TestAStar(unittest.TestCase):
    # As we cannot predict the exact path A* will take (often there are multiple optimum routes) we'll check length of returned path arrays instead
    # Start with checking a simple 2x2 grid path length is 3
    # Check 3x3 grid from one corner to another path length is 5
    def test_a_star_path(self):
        # Check path lengths to ensure A* is getting optimum routes
        # Check 2x2 grid path length is 3 (optimum)
        self.assertEqual(len(a_star_path([0, 0], [1, 1], 2, 2, [])), 3)

        # Check 3x3 grid path length is 5 (optimum)
        self.assertEqual(len(a_star_path([0, 0], [2, 2], 3, 3, [])), 5)

        # Check 8x8 grid path length is 15 (optimum)
        self.assertEqual(len(a_star_path([0, 0], [7, 7], 8, 8, [])), 15)

        # Check that the function is returning the paths in the correct data structure form
        self.assertEqual(a_star_path(
            [0, 0], [0, 1], 1, 2, []), [[0, 0], [0, 1]])

        # Check that we are still finding optimum paths around the snakes body
        # Place a snake body block in the middle of top left and top right corner of a 3x3
        self.assertEqual(a_star_path([0, 0], [2, 0], 3, 3, [[1, 0]]), [
                         [0, 0], [0, 1], [1, 1], [2, 1], [2, 0]])

        # Place a snake body block down the top middle - path has to go in an L shape
        self.assertEqual(a_star_path([0, 0], [2, 2], 3, 3, [[1, 0], [1, 1]]), [
                         [0, 0], [0, 1], [0, 2], [1, 2], [2, 2]])

        # Check that the path returns None when there are no possible routes
        # Place a snake body block all the way across the middle of the grid
        self.assertIsNone(a_star_path(
            [0, 0], [2, 2], 3, 3, [[0, 1], [1, 1], [2, 1]]))

        # Give the algorithm nonsensical environment values
        self.assertIsNone(a_star_path([-1, -1], [4, 5], 3, 3, []))


if __name__ == '__main__':
    unittest.main()
