import pygame
from gameparams import GameParams


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.update_cam_coordinate(0, 0)

        self.x = 0
        self.y = 0

        self.tile_offset = (0, 0)

    def debug_obj(self):
        return {
            'x': self.x,
            'y': self.y,
            'tile_offset': self.tile_offset,
        }

    def update_cam_coordinate(self, x, y):
        self.camera = pygame.Rect(x, y, self.width, self.height)

    def apply(self, e):
        return e.rect.move(self.camera.topleft)

    def update_tile_offset(self, player):
        self.tile_offset = (
            self.tile_offset[0] + player.last_vector[0],
            self.tile_offset[1] + player.last_vector[1]
        )

    def update(self, player):
        self.x = -player.param['pixel_x'] + \
            int(GameParams.Window.Width / 2) + 30
        self.y = -player.param['pixel_y'] + \
            int(GameParams.Window.Height / 2) + 30
        self.update_cam_coordinate(self.x, self.y)
