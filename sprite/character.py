import logging
import math
import pygame

from sprite.sprite import Sprite
from display.grid import Grid

logger = logging.getLogger()


class Character(Sprite):
    def __init__(self, surface, image, x_coordinate=0, y_coordinate=0):
        Sprite.__init__(self, surface,  image, x_coordinate=x_coordinate,
                        y_coordinate=y_coordinate, w=32, h=32)
        self.velocity = 2
        self.moving = False
        self.instance_name = 'none'

    def debug_obj(self):
        return {
            'moving': self.moving,
        }

    def move(self, x, y):
        self.last_vector = [x ,y]
        if not self.check_wall_collision(x, y):
            logger.debug(f"[{self.instance_name}] \
                ({self.param['x_coordinate'], self.param['y_coordinate']}) -> ({x}, {y})")
            self.param['x_coordinate'] = x
            self.param['y_coordinate'] = y

            self.get_drawpoint()
            self.param['ready'] = False
            self.moving = True

    def get_drawpoint(self):
        (self.param['x_final'], self.param['y_final']) = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])
