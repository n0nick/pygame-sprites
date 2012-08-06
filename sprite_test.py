import unittest
import pygame
from pygame.locals import *
import os

# Import new sprite class
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
from sprite import *

class SpriteTests(unittest.TestCase):

    def setUp(self):
        self.shared_stuff = 1
        self.s1 = Sprite()
        self.s1.rect = Rect((0, 0, 0, 0))
        self.s1.position = (0, 0)

    def test_sanity(self):
        self.assertEqual(self.shared_stuff, 1)

    def test_move_to(self):
        self.s1.move_to((0, 0))
        self.assertEqual(self.s1.position, (0, 0))
        self.s1.move_to((52, 24))
        self.assertEqual(self.s1.position, (52, 24))

    def test_move_by(self):
        self.s1.move_by((0, 0))
        self.assertEqual(self.s1.position, (0, 0))
        self.s1.move_by((2, 4))
        self.assertEqual(self.s1.position, (2, 4))
        self.s1.move_by((3, 3))
        self.assertEqual(self.s1.position, (5, 7))

if __name__ == '__main__':
    unittest.main()
