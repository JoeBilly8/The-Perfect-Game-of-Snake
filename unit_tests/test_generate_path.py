import unittest
from snake_ai_functions.generate_path import path


class TestPath(unittest.TestCase):
    # Check all wall functions

    # "Generate" a known Prim's maze for our functions
    # This is the 3x3 maze I have commonly used in many of my examples + explanations (diss)
    maze = [[(0, 0), 'bottom', 'right'], [(0, 1), 'top', 'bottom', 'right'], [(1, 0), 'left', 'right'], [(0, 2), 'top', 'right'],
            [(1, 2), 'left', 'right'], [(2, 0), 'left'], [(1, 1), 'left', 'right'], [(2, 2), 'left'], [(2, 1), 'left']]

    def test_is_wall_right(self):
        # Create path object for use of it's functions
        p = path(6, 6)
        # # # Check a true and false return of if the wall is right for each of our 4 directions
        #  # Should return true
        # North
        self.assertTrue(p.is_wall_right(self.maze, "NORTH", (0, 0), [0, 1]))
        # East
        self.assertTrue(p.is_wall_right(self.maze, "EAST", (0, 0), [1, 0]))
        # South
        self.assertTrue(p.is_wall_right(self.maze, "SOUTH", (0, 0), [1, 1]))
        # West
        self.assertTrue(p.is_wall_right(self.maze, "WEST", (0, 0), [1, 1]))

        # # Should return false
        # North
        self.assertFalse(p.is_wall_right(self.maze, "NORTH", (0, 0), [0, 0]))
        # East
        self.assertFalse(p.is_wall_right(self.maze, "EAST", (0, 0), [0, 0]))
        # South
        self.assertFalse(p.is_wall_right(self.maze, "SOUTH", (0, 0), [1, 0]))
        # West
        self.assertFalse(p.is_wall_right(self.maze, "WEST", (0, 0), [1, 0]))

    def test_is_wall_infront(self):
        # Create path object for use of it's functions
        p = path(6, 6)
        # # # Check a true and false return of if the wall is right for each of our 4 directions
        # # Should return true
        # North
        self.assertTrue(p.is_wall_infront(self.maze, "NORTH", (0, 0), [1, 1]))
        # East
        self.assertTrue(p.is_wall_infront(self.maze, "EAST", (0, 0), [0, 1]))
        # South
        self.assertTrue(p.is_wall_infront(self.maze, "SOUTH", (0, 0), [1, 0]))
        # West
        self.assertTrue(p.is_wall_infront(self.maze, "WEST", (0, 0), [1, 1]))

        # # Should return false
        # North
        self.assertFalse(p.is_wall_infront(self.maze, "NORTH", (0, 0), [0, 1]))
        # East
        self.assertFalse(p.is_wall_infront(self.maze, "EAST", (0, 0), [0, 0]))
        # South
        self.assertFalse(p.is_wall_infront(self.maze, "SOUTH", (0, 0), [0, 0]))
        # West
        self.assertFalse(p.is_wall_infront(self.maze, "WEST", (0, 0), [1, 0]))

    def test_is_edge_right(self):
        # Create path object for use of it's functions
        p = path(6, 6)
        # # # Check a true and false return of if the edge is right for each of our 4 directions
        # # Should return true
        # North
        self.assertTrue(p.is_edge_right(6, 6, "NORTH", [1, 1], (5, 5)))
        # East
        self.assertTrue(p.is_edge_right(6, 6, "EAST", [0, 1], (5, 5)))
        # South
        self.assertTrue(p.is_edge_right(6, 6, "SOUTH", [0, 0], (0, 0)))
        # West
        self.assertTrue(p.is_edge_right(6, 6, "WEST", [1, 0], (0, 0)))

        # # Should return false
        # North
        self.assertFalse(p.is_edge_right(6, 6, "NORTH", [0, 1], (0, 0)))
        # East
        self.assertFalse(p.is_edge_right(6, 6, "EAST", [0, 0], (0, 0)))
        # South
        self.assertFalse(p.is_edge_right(6, 6, "SOUTH", [1, 0], (5, 5)))
        # West
        self.assertFalse(p.is_edge_right(6, 6, "WEST", [1, 1], (5, 5)))

    def test_is_edge_infront(self):
        # Create path object for use of it's functions
        p = path(6, 6)
        # # # Check a true and false return of if the edge is right for each of our 4 directions
        # # Should return true
        # North
        self.assertTrue(p.is_edge_infront(6, 6, "NORTH", [0, 0], (0, 0)))
        # East
        self.assertTrue(p.is_edge_infront(6, 6, "EAST", [1, 1], (5, 5)))
        # South
        self.assertTrue(p.is_edge_infront(6, 6, "SOUTH", [1, 1], (5, 5)))
        # West
        self.assertTrue(p.is_edge_infront(6, 6, "WEST", [0, 0], (0, 0)))

        # # Should return false
        # North
        self.assertFalse(p.is_edge_infront(6, 6, "NORTH", [0, 1], (0, 0)))
        # East
        self.assertFalse(p.is_edge_infront(6, 6, "EAST", [0, 0], (0, 0)))
        # South
        self.assertFalse(p.is_edge_infront(6, 6, "SOUTH", [1, 0], (5, 5)))
        # West
        self.assertFalse(p.is_edge_infront(6, 6, "WEST", [1, 1], (5, 5)))

    def test_can_go_right(self):
        # Create path object for use of it's functions
        p = path(6, 6)
        # # # Check known boundary cases both with the edges and the walls for all directions
        # # Should return true
        # North
        self.assertTrue(p.can_go_right(
            self.maze, "NORTH", (0, 0), [0, 0], 6, 6))
        # East
        self.assertTrue(p.can_go_right(
            self.maze, "EAST", (2, 0), [1, 0], 6, 6))
        # South
        self.assertTrue(p.can_go_right(
            self.maze, "SOUTH", (2, 0), [1, 1], 6, 6))
        # West
        self.assertTrue(p.can_go_right(
            self.maze, "WEST", (0, 2), [0, 1], 6, 6))

        # # # Should return false
        # North
        self.assertFalse(p.can_go_right(
            self.maze, "NORTH", (0, 0), [0, 1], 6, 6))
        # East
        self.assertFalse(p.can_go_right(
            self.maze, "EAST", (2, 0), [0, 0], 6, 6))
        # South
        self.assertFalse(p.can_go_right(
            self.maze, "SOUTH", (0, 0), [0, 0], 6, 6))
        # West
        self.assertFalse(p.can_go_right(
            self.maze, "WEST", (0, 0), [0, 0], 6, 6))

    def test_can_go_forward(self):
        # Create path object for use of it's functions
        p = path(6, 6)
        # # # Check known boundary cases both with the edges and the walls for all directions
        # # Should return true
        # North
        self.assertTrue(p.can_go_forward(
            self.maze, "NORTH", (0, 0), [0, 1], 6, 6))
        # East
        self.assertTrue(p.can_go_forward(
            self.maze, "EAST", (0, 0), [1, 0], 6, 6))
        # South
        self.assertTrue(p.can_go_forward(
            self.maze, "SOUTH", (0, 0), [0, 1], 6, 6))
        # West
        self.assertTrue(p.can_go_forward(
            self.maze, "WEST", (0, 0), [1, 0], 6, 6))

        # # Should return false
        # North
        self.assertFalse(p.can_go_forward(
            self.maze, "NORTH", (0, 0), [0, 0], 6, 6))
        # East
        self.assertFalse(p.can_go_forward(
            self.maze, "EAST", (0, 0), [0, 1], 6, 6))
        # South
        self.assertFalse(p.can_go_forward(
            self.maze, "SOUTH", (0, 0), [1, 0], 6, 6))
        # West
        self.assertFalse(p.can_go_forward(
            self.maze, "WEST", (0, 0), [0, 0], 6, 6))

    def test_generate_path(self):
        p = path(6, 6)

        # Because the randomness of the hamiltonian comes from the prims maze, using a known maze allows us to know the path ahead of time
        # Check that the function is returning the paths in the correct data structure form
        self.assertEqual(p.generate_path(self.maze), [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (
            5, 3), (4, 3), (3, 3), (2, 3), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1)])

        # Path is of expected length in a 6x6
        self.assertEqual(len(p.generate_path(self.maze)), 36)

        # Check path is of expected length in a 12x12
        p2 = path(12, 12)
        self.assertEqual(len(p2.generate_path(self.maze)), 144)


if __name__ == '__main__':
    unittest.main()
