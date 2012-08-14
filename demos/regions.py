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
data_dir = os.path.join(main_dir, 'data')

SCREENSIZE = 700
REGIONSROW = 7
REGIONSROWIZE = SCREENSIZE / REGIONSROW

colors = {
    "background": pygame.Color(225, 225, 225),
    "point": pygame.Color(0, 0, 0)
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
    return image


class Ball(Sprite):
    def __init__(self, regions):
        Sprite.__init__(self)
        self.set_image(load_image("ball.png", -1))
        self.regions = regions
        self.current_region = 0
        self.draw_in_region()

    def move(self, direction):
        if direction:
            if direction == pygame.K_RIGHT:
                self.current_region += 1
            elif direction == pygame.K_LEFT:
                self.current_region -= 1
            elif direction == pygame.K_UP:
                self.current_region -= REGIONSROW
            elif direction == pygame.K_DOWN:
                self.current_region += REGIONSROW

        self.current_region %= len(self.regions)
        self.draw_in_region()

    def change_anchor(self, key):
        if key == pygame.K_a:
            self.anchor = ANCHOR_TOPLEFT
        elif key == pygame.K_s:
            self.anchor = ANCHOR_CENTER
        elif key == pygame.K_d:
            self.anchor = (25, 20)

    def draw_in_region(self):
        self.move_to(self.regions[self.current_region])


def print_labels(screen, regions):
    font = pygame.font.Font(None, 14)
    for x, y in regions:
        if x > 0 and y > 0:  # labels
            text = font.render("{0},{1}".format(x, y), 1, colors["point"])
            textpos = text.get_rect(centerx=x, centery=y)
            screen.blit(text, textpos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))
    clock = pygame.time.Clock()
    arrow_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    anchor_keys = [pygame.K_a, pygame.K_s, pygame.K_d]
    quit_keys = [pygame.K_ESCAPE, pygame.K_q]

    # background
    background = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    background = background.convert()
    background.fill(colors["background"])

    # prepare regions
    regions = []
    for i in range(0, REGIONSROW):
        y = i * REGIONSROWIZE
        for j in range(0, REGIONSROW):
            x = j * REGIONSROWIZE
            regions.append((x, y))

    # add ball sprite
    ball = Ball(regions)
    all = pygame.sprite.RenderPlain((ball))

    try:
        while 1:

            for event in pygame.event.get():
                if event.type == QUIT:
                        return
                if event.type == pygame.KEYUP:
                    if event.key in arrow_keys:
                        ball.move(event.key)
                    elif event.key in anchor_keys:
                        ball.change_anchor(event.key)
                    elif event.key in quit_keys:
                        return

            all.clear(screen, background)
            all.update()

            screen.blit(background, (0, 0))
            print_labels(screen, regions)

            all.draw(screen)
            pygame.display.flip()
            clock.tick(40)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
