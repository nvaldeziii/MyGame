import pygame
from sprite import Sprite
from grid import Grid


class WorldTile:
    pass

class Tile(Sprite):
    def __init__(self, surface, image):
        self.tile_w = 100
        self.tile_h = 50
        Sprite.__init__(self, surface, image, w=self.tile_w, h=self.tile_h, )

    def update(self):
        for x in range(0, 11):
            for y in range(0, 23):
                self.update_coordinate(x, y)
                self.rect.center= (self.param['pixel_x'], self.param['pixel_y'])
                self.surface.blit(self.image, self.rect)
