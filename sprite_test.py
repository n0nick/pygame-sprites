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

    def test_set_image(self):
        #TODO
        pass

    def test_update_image(self):
        #TODO
        pass

    def test_set_offset(self):
        self.s1.move_to((0, 0))
        self.s1.set_offset((25, 25))
        self.assertEqual(self.s1.rect.topleft, (25, 25))
        self.s1.move_to((12, 12))
        self.assertEqual(self.s1.rect.topleft, (37, 37))
        self.s1.set_offset((7, 7))
        self.assertEqual(self.s1.rect.topleft, (19, 19))

    def test_make_visible(self):
        #TODO
        pass

    def test_make_invisible(self):
        #TODO
        pass

    def test_toggle_visibility(self):
        self.s1.make_visible()
        self.s1.toggle_visibility()
        self.assertEqual(self.s1.visible, False)
        self.s1.toggle_visibility()
        self.assertEqual(self.s1.visible, True)

    def test_rotate_to(self):
        #TODO
        pass

    def test_rotate_by(self):
        #TODO
        pass

    def test_scale_to(self):
        #TODO
        pass

    def test_scale_by(self):
        #TODO
        pass

class AggregatedSpriteTests(unittest.TestCase):
    def setUp(self):
        self.s = AggregatedSprite()

    def test_add_sprite(self):
        s1 = Sprite()
        s1.rect = Rect((0, 0, 0, 0))
        s1.position = (0, 0)
        self.s.add_sprite(s1)
        self.assertEqual(self.s.sprites, [s1])
        s2 = Sprite()
        s2.rect = Rect((0, 0, 0, 0))
        s2.position = (0, 0)
        self.s.add_sprite(s2)
        self.assertEqual(self.s.sprites, [s1, s2])

    def test_draw(self):
        #TODO
        pass

    def test_propagate(self):
        #TODO
        pass


if __name__ == '__main__':
    unittest.main()
