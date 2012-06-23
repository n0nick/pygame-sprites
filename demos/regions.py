#!/usr/bin/env python

import pygame
from pygame.locals import *
from pygame.compat import geterror
import os

if not pygame.font:
    print ("No font support compiled")
    sys.exit()

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = main_dir

SCREENSIZE = 700
REGIONS = 7
REGIONSIZE = SCREENSIZE / REGIONS

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
    return image, image.get_rect()


class Ball(pygame.sprite.Sprite):
    def __init__(self, regions):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("ball.png", -1)
        self.regions = regions
        self.current_region = 0
        self.draw_in_region()

    def move(self, direction):
        if direction:
            if direction > 0:
                self.current_region += 1
            if direction < 0:
                self.current_region -= 1
        self.current_region %= len(self.regions)
        self.draw_in_region()

    def draw_in_region(self):
        self.rect.topleft = self.regions[self.current_region]


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))
    clock = pygame.time.Clock()
    screen.fill(colors["background"])
    background = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    font = pygame.font.Font(None, 14)
    regions = []

    # prepare regions and label them
    for i in range(0, REGIONS):
        y = i * REGIONSIZE
        for j in range(0, REGIONS):
            x = j * REGIONSIZE
            regions.append((x, y))
            if x > 0 and y > 0:  # labels
                text = font.render("{0},{1}".format(x, y), 1, colors["point"])
                textpos = text.get_rect(centerx=x, centery=y)
                screen.blit(text, textpos)

    # add ball sprite
    ball = Ball(regions)
    all = pygame.sprite.RenderPlain((ball))

    try:
        while 1:

            for event in pygame.event.get():
                if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                        return

            keystate = pygame.key.get_pressed()

            direction = keystate[K_RIGHT] - keystate[K_LEFT]
            if direction:
                ball.move(direction)

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
