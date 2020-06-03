import pygame
from config.gameparams import GameParams


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.x = 0
        self.y = 0

    def debug_obj(self):
        return {
            'x': self.x,
            'y': self.y,
        }

    def update_cam_coordinate(self, x, y):
        self.camera = pygame.Rect(x, y, self.width, self.height)

    def apply(self, e):
        return e.rect.move(self.camera.topleft)

    def update(self, player):
        self.x = -player.param['pixel_x'] + \
            int(GameParams.config['window']['resolution']['width'] / 2) + 30
        self.y = -player.param['pixel_y'] + \
            int(GameParams.config['window']['resolution']['height'] / 2) + 30
        self.update_cam_coordinate(self.x, self.y)
