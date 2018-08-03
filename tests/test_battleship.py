# Run with python3 -m unittest test_battleship.py
import unittest
from torpydo import ships
from torpydo.ships import Point


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = ships.Ship("TestShip", 4, "White")

    def test_is_at(self):
        self.ship.all_positions.add(Point(1, 2))

        self.assertTrue(self.ship.receive_fire(Point(1, 2)))


if '__main__' == __name__:
    unittest.main()


# test comment hi
