import unittest
from grid import Grid


class TestGrid(unittest.TestCase):
    def test_get_movement_vector_left(self):
        x, y = Grid.get_movement_vector(4, 0, 6, 0, 1)
        self.assertAlmostEqual(x, 5)
        self.assertAlmostEqual(y, 0)

    def test_get_movement_vector_right(self):
        x, y = Grid.get_movement_vector(6, 0, 4, 0, 1)
        self.assertAlmostEqual(x, 5)
        self.assertAlmostEqual(y, 0)

    def test_get_movement_vector_down(self):
        print("********")
        x, y = Grid.get_movement_vector(0,1, 0, 2, 1)
        print(f"x = {x}")
        print(f"y = {y}")
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y, 2)


if __name__ == '__main__':
    unittest.main()
