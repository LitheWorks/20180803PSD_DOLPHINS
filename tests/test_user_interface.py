# Run with python3 -m unittest test_user_interface.py
import unittest
from torpydo.user_interface import Color, colorfy


class TestShip(unittest.TestCase):
    def test_colorfy(self):
        msg = colorfy("Hello", Color.white_on_blue)
        self.assertEqual("\x1b[1;37;44mHello\x1b[0m", msg)


if '__main__' == __name__:
    unittest.main()
