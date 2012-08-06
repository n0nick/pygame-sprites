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

    def test_sanity(self):
        self.assertEqual(self.shared_stuff, 1)

if __name__ == '__main__':
    unittest.main()
