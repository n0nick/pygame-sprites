#!/usr/bin/env python

import os
import pygame
from pygame.locals import *
from pygame.compat import geterror

# Import new sprite class
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
from sprite import *

if not pygame.font:
    print ("No font support compiled")
    sys.exit()

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = main_dir

SCREENSIZE = 700
SCREENCENTER = (SCREENSIZE / 2, SCREENSIZE / 2)

colors = {
        "background": pygame.Color(225, 225, 225),
        "square": pygame.Color(0, 0, 0)
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


def draw_squares(screen):
    line_length = 5
    for size in [100, 250, 500]:
        for sgn_x in [+1, -1]:
            for sgn_y in [+1, -1]:
                x = SCREENSIZE / 2 + sgn_x * size / 2
                y = SCREENSIZE / 2 + sgn_y * size / 2
                pygame.draw.lines(screen, colors["square"], False,
                        [(x, y - sgn_y * line_length),
                         (x, y),
                         (x - sgn_x * line_length, y)])


class Ball(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image, self.rect = load_image("ball.png", -1)
        self.anchor = ANCHOR_CENTER


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))
    clock = pygame.time.Clock()
    quit_keys = [pygame.K_ESCAPE, pygame.K_q]

    # background
    background = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    background = background.convert()
    background.fill(colors["background"])

    # add ball sprite
    ball = Ball()
    ball.position = SCREENCENTER
    all = pygame.sprite.RenderPlain((ball))

    try:
        while 1:

            for event in pygame.event.get():
                if event.type == QUIT:
                        return
                if event.type == pygame.KEYUP:
                    if event.key in quit_keys:
                        return

            all.clear(screen, background)
            all.update()

            screen.blit(background, (0, 0))
            draw_squares(screen)

            all.draw(screen)
            pygame.display.flip()
            clock.tick(40)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
