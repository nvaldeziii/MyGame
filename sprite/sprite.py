import pygame
import logging
from display.grid import Grid


logger = logging.getLogger()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, surface, image, x_coordinate=0, y_coordinate=0, w=64, h=64, ):
        super().__init__()
        self.surface = surface
        self.param = {
            'x_coordinate': x_coordinate,
            'y_coordinate': y_coordinate,
            'old_coordinate': (0, 0),
            'w': w,
            'h': h,
            'ready': True,
            'x_final': 0,
            'y_final': 0,
            'pixel_x': 0,
            'pixel_y': 0
        }
        self.rect = pygame.Rect(x_coordinate, y_coordinate, w, h)

        try:
            self.image = pygame.image.load(image)
        except pygame.error as e:
            self.image = pygame.image.load(
                'assets/sprites/tile/floor/placeholder_01.png')
            logger.warning(f"{e}")

        self.param['pixel_x'], self.param['pixel_y'] = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])
        (self.param['x_final'], self.param['y_final']) = (
            self.param['pixel_x'], self.param['pixel_y'])

        self.get_drawpoint()

    def update_rect(self, dx, dy):
        raise NotImplementedError()

    def get_drawpoint(self):
        (self.param['pixel_x'], self.param['pixel_y']) = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])

    def update(self):
        self.rect.center = (self.param['pixel_x'], self.param['pixel_y'])
        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)

    def update_coordinate(self, x_coordinate, y_coordinate):
        self.param['x_coordinate'] = x_coordinate
        self.param['y_coordinate'] = y_coordinate
        self.get_drawpoint()
