#!/usr/bin/env python

import os
import pygame
from pygame.locals import *
from pygame.compat import geterror

# Import new sprite class
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
from sprite import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

SCREEN_SIZE = 700

colors = {
        "background": pygame.Color(225, 225, 225),
}


def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


class Thing(Sprite):
    def __init__(self, filename):
        Sprite.__init__(self)
        self.image, self.rect = load_image(filename + ".png", -1)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pygame.time.Clock()
    layer_keys = [pygame.K_1, pygame.K_2, pygame.K_3]
    quit_keys = [pygame.K_ESCAPE, pygame.K_q]

    # background
    background = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    background = background.convert()
    background.fill(colors["background"])

    # add ball sprite
    ball = Thing("ball")
    ball.position = (10, 10)
    ball.layer = 1
    button = Thing("button")
    button.position = (30, 30)
    button.layer = 2
    teddy = Thing("teddy")
    teddy.position = (50, 50)
    teddy.layer = 3
    all = Group((ball, button, teddy))

    try:
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == pygame.KEYUP:
                    if event.key in layer_keys:
                        if event.key == pygame.K_1:
                            ball.layer = 1
                            button.layer = 2
                            teddy.layer = 3
                        elif event.key == pygame.K_2:
                            ball.layer = 2
                            button.layer = 3
                            teddy.layer = 1
                        elif event.key == pygame.K_3:
                            ball.layer = 3
                            button.layer = 1
                            teddy.layer = 2
                        all.remove((ball, button, teddy))
                        all.add((ball, button, teddy))
                    elif event.key in quit_keys:  # quit game
                        return

            all.clear(screen, background)
            all.update()

            screen.blit(background, (0, 0))

            all.draw(screen)
            pygame.display.flip()
            clock.tick(40)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
