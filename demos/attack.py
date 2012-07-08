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
data_dir = main_dir

SCREENSIZE = 700
BALL_ROWS = 3
BALL_COLS = 5
BALL_SIZE = 100
SCALE_STEP = 0.1
SCALE_MIN = 0.3
SCALE_MAX = 3.0
ROTATE_STEP = 5
MOVE_STEP = 5
X_MAX = SCREENSIZE - (BALL_COLS + 1) * BALL_SIZE
Y_MAX = SCREENSIZE - (BALL_ROWS + 1) * BALL_SIZE

colors = {
        "background": pygame.Color(225, 225, 225)
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


class Ball(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image, self.rect = load_image("ball.png", -1)
        self.anchor = ANCHOR_CENTER


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))
    clock = pygame.time.Clock()
    rotate_keys = [pygame.K_a, pygame.K_s]
    scale_keys = [pygame.K_z, pygame.K_x]
    visibility_keys = [pygame.K_SPACE]
    left_keys = [pygame.K_LEFT, pygame.K_RIGHT]
    top_keys = [pygame.K_UP, pygame.K_DOWN]
    quit_keys = [pygame.K_ESCAPE, pygame.K_q]

    # background
    background = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    background = background.convert()
    background.fill(colors["background"])

    # add ball sprite
    balls = AggregatedSprite()
    for i in range(0, BALL_COLS):
        for j in range(0, BALL_ROWS):
            b = Ball()
            b.position = (BALL_SIZE + i * BALL_SIZE, BALL_SIZE + j * BALL_SIZE)
            balls.add_sprite(b)
    all = RenderPlain((balls))

    scale, rotate, top, left = 0, 0, 0, 0
    try:
        while 1:

            for event in pygame.event.get():
                if event.type == QUIT:
                        return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        rotate = 1
                    elif event.key == pygame.K_s:
                        rotate = -1
                    elif event.key == pygame.K_z:
                        scale = 1
                    elif event.key == pygame.K_x:
                        scale = -1
                    elif event.key == pygame.K_UP:
                        top = -1
                    elif event.key == pygame.K_DOWN:
                        top = 1
                    elif event.key == pygame.K_LEFT:
                        left = -1
                    elif event.key == pygame.K_RIGHT:
                        left = 1
                elif event.type == pygame.KEYUP:
                    if event.key in rotate_keys:
                        rotate = 0
                    elif event.key in scale_keys:
                        scale = 0
                    elif event.key in left_keys:
                        left = 0
                    elif event.key in top_keys:
                        top = 0
                    elif event.key in visibility_keys:
                        balls.visible = not balls.visible
                    elif event.key in quit_keys:
                        return

            if scale != 0:
                new_scale = balls.scale + SCALE_STEP * scale
                if SCALE_MIN < new_scale < SCALE_MAX:
                    balls.scale = new_scale

            if rotate != 0:
                balls.rotate += rotate * ROTATE_STEP

            if left != 0 or top != 0:
                (x, y) = balls.position
                x += left * MOVE_STEP
                y += top * MOVE_STEP

                if 0 <= x <= X_MAX:
                    if 0 <= y <= Y_MAX:
                        balls.position = (x, y)

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
