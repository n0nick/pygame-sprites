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
        self.s1.set_image(pygame.Surface((10, 10)))
        self.assertEqual(self.s1.rect.size, (10, 10))
        self.s1.set_image(pygame.Surface((28, 93)))
        self.assertEqual(self.s1.rect.size, (28, 93))

    def test_update_image(self):
        self.s1.image = self.s1.original = pygame.Surface((13, 19))
        self.s1.update_image()
        self.assertEqual(self.s1.rect.size, (13, 19))

    def test_set_offset(self):
        self.s1.move_to((0, 0))
        self.s1.set_offset((25, 25))
        self.assertEqual(self.s1.rect.topleft, (25, 25))
        self.s1.move_to((12, 12))
        self.assertEqual(self.s1.rect.topleft, (37, 37))
        self.s1.set_offset((7, 7))
        self.assertEqual(self.s1.rect.topleft, (19, 19))

    def test_make_visible_invisible(self):
        surface = pygame.Surface((20, 20))
        self.s1.set_image(pygame.Surface((10, 10)))
        self.s1.image.fill(pygame.Color('red'))
        self.s1.make_invisible()
        self.assertEqual(self.s1.visible, False)
        self.assertEqual(self.s1.draw(surface), 0)
        self.s1.make_visible()
        self.assertEqual(self.s1.visible, True)
        self.assertNotEqual(self.s1.draw(surface), 0)

    def test_toggle_visibility(self):
        self.s1.make_visible()
        self.s1.toggle_visibility()
        self.assertEqual(self.s1.visible, False)
        self.s1.toggle_visibility()
        self.assertEqual(self.s1.visible, True)

    def test_rotate_to(self):
        # prepare bg surface
        surface = pygame.Surface((100, 100))
        surface.fill(pygame.Color('white'))
        # prepare sprite
        self.s1.set_image(pygame.Surface((32, 32), pygame.SRCALPHA))
        # paint the sprite half red, half blue
        self.s1.image.fill(pygame.Color('red'), pygame.Rect(0, 0, 16, 32))
        self.s1.image.fill(pygame.Color('blue'), pygame.Rect(16, 0, 32, 32))
        # draw sprite on surface
        self.s1.draw(surface)
        self.s1.move_to((0, 0))

        # sanity-check colors
        self.assertEqual(surface.get_at((5, 5)), pygame.Color('red'))

        # rotate sprite
        self.s1.rotate_to(180)
        self.s1.draw(surface)
        self.assertEqual(surface.get_at((5, 5)), pygame.Color('blue'))
        pass

    def test_rotate_by(self):
        self.s1.set_image(pygame.Surface((15, 45)))
        self.assertEqual(self.s1.rotate, 0)
        self.s1.rotate_by(15)
        self.assertEqual(self.s1.rotate, 15)
        self.s1.rotate_by(15)
        self.assertEqual(self.s1.rotate, 30)
        self.s1.rotate_by(390)
        self.assertEqual(self.s1.rotate, 60)

    def test_scale_to(self):
        self.s1.set_image(pygame.Surface((10, 10)))
        self.assertEqual(self.s1.rect.size, ((10, 10)))
        self.s1.scale_to(3)
        self.assertEqual(self.s1.rect.size, ((30, 30)))
        self.s1.scale_to(0.7)
        self.assertEqual(self.s1.rect.size, ((7, 7)))

    def test_scale_by(self):
        self.s1.set_image(pygame.Surface((10, 10)))
        self.assertEqual(self.s1.rect.size, ((10, 10)))
        self.s1.scale_by(3)
        self.assertEqual(self.s1.rect.size, ((40, 40)))
        self.s1.scale_by(0.7)
        self.assertEqual(self.s1.rect.size, ((47, 47)))
        self.s1.scale_by(-2)
        self.assertEqual(self.s1.rect.size, ((27, 27)))


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
        # prepare sprites
        s1 = Sprite()
        s1.set_image(pygame.Surface((10, 10)))
        s1.move_to((0, 0))
        s2 = Sprite()
        s2.set_image(pygame.Surface((23, 23)))
        s2.move_to((3, 3))
        # add to aggregated sprite
        self.s.add_sprite(s1)
        self.s.add_sprite(s2)
        # some sanity-checks
        self.assertEqual(s1.rect.topleft, (0, 0))
        self.assertEqual(s2.rect.topleft, (3, 3))
        self.assertEqual(s1.rect.size, (10, 10))
        self.assertEqual(s2.rect.size, (23, 23))
        # propagate move events
        self.s.move_to((6, 6))
        self.assertEqual(s1.rect.topleft, (6, 6))
        self.assertEqual(s2.rect.topleft, (9, 9))
        self.s.move_by((1, 3))
        self.assertEqual(s1.rect.topleft, (7, 9))
        self.assertEqual(s2.rect.topleft, (10, 12))
        # propagate scale events
        self.s.scale_to(3)
        self.assertEqual(s1.rect.size, (30, 30))
        self.assertEqual(s2.rect.size, (69, 69))
        self.s.scale_by(2)
        self.assertEqual(s1.rect.size, (50, 50))
        self.assertEqual(s2.rect.size, (115, 115))


if __name__ == '__main__':
    unittest.main()
