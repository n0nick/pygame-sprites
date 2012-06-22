#!/usr/bin/env python

import pygame
import pygame.gfxdraw
from pygame.locals import *
from pygame.compat import geterror
from pygame import gfxdraw
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = main_dir

SCREENSIZE = 700
REGIONS = 7
REGIONSIZE = SCREENSIZE / REGIONS
BGCOLOR = (225, 225, 225)
POINTCOLOR = (0, 0, 0)


def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("ball.png", -1)
        self.rect.topleft = 10, 10


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))
    screen.fill(BGCOLOR)
    bg = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)

    # draw region limits
    for i in range(1, REGIONS):
        x = i * REGIONSIZE
        for j in range(1, REGIONS):
            y = j * REGIONSIZE
            pygame.gfxdraw.pixel(bg, x, y, POINTCOLOR)

    # add ball sprite
    ball = Ball()
    allsprites = pygame.sprite.RenderPlain((ball))

    try:
        while 1:

            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break

            allsprites.update()
            screen.blit(bg, (0, 0))
            allsprites.draw(screen)
            pygame.display.flip()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()
