import unittest
from snake_main import snake


class TestSnake(unittest.TestCase):
    def test_add_arrays(self):
        # Standard
        self.assertEqual(snake.addArrays([1, 2], [3, 4]), [4, 6])
        # Zero Values
        self.assertEqual(snake.addArrays([0, 0], [0, 0]), [0, 0])
        # Negative Values
        self.assertEqual(snake.addArrays([-1, -2], [-1, -2]), [-2, -4])

    def test_draw(self):
        pass

    def test_move(self):
        pass

    def test_grow(self):
        pass


if __name__ == '__main__':
    unittest.main()
