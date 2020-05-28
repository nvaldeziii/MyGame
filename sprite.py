import pygame
from grid import Grid


class Sprite:
    def __init__(self, surface=None, x_coordinate=0, y_coordinate=0, w=64, h=64):
        self.surface = surface
        self.param = {
            'x_coordinate': x_coordinate,
            'y_coordinate': y_coordinate,
            'old_coordinate': (0,0),
            'w': w,
            'h': h,
            'ready': True,
            'x_final': 0,
            'y_final': 0,
            'pixel_x': 0,
            'pixel_y': 0
        }
        self.rect = pygame.Rect(x_coordinate, y_coordinate, w, h)

        self.param['pixel_x'], self.param['pixel_y'] = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])
        (self.param['x_final'], self.param['y_final']) = (self.param['pixel_x'], self.param['pixel_y'])

        self.get_drawpoint()

    def get_drawpoint(self):
        self.param['old_coordinate'] = (self.param['pixel_x'], self.param['pixel_y'])
        (self.param['pixel_x'], self.param['pixel_y']) = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])

    def draw(self):
        centerpixel = (self.param['pixel_x'] - (self.param['w']/2), self.param['pixel_y'] - self.param['h'])
        pygame.draw.rect(self.surface, (255, 0, 0), (
            centerpixel[0],
            centerpixel[1],
            self.param['w'],
            self.param['h']
        ))

    def update_coordinate(self, x_coordinate, y_coordinate):
        self.param['x_coordinate'] = x_coordinate
        self.param['y_coordinate'] = y_coordinate
        self.get_drawpoint()
