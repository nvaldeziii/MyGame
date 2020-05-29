import pygame
from sprite import Sprite
from grid import Grid
from display import Display


class WorldTile:
    def __init__(self, surface=Display.Surface['tile'], sprite_group=Display.Group['tile']):
        self.surface = surface
        self.sprite_group = sprite_group
        self.mapinfo = MapInfo()
        self.topleft = [0, 0]

    def generate_area(self):
        x = 0
        y = 0
        for i in range(0, self.mapinfo.tiles_total):
            if i % self.mapinfo.max_x == 0:
                x = 0
                y += 1
            tile = Tile(self.surface, self.mapinfo.tiles[i]['img'])
            tile.update_coordinate(x,y)
            self.sprite_group.add(tile)
            x += 1


class MapInfo:
    ONE_TILE = {
        'img': 'sprites/tile/sample.png'
    }

    def __init__(self, max_x=16):
        self.max_x = max_x
        self.tiles_total = self.max_x ** 2
        self.tiles = [MapInfo.ONE_TILE] * self.tiles_total


class Tile(Sprite):
    def __init__(self, surface, image):
        self.tile_w = 100
        self.tile_h = 50
        Sprite.__init__(self, surface, image, w=self.tile_w, h=self.tile_h, )

    def update(self):
        # self.update_coordinate(x, y)
        self.rect.center = (
            self.param['pixel_x'], self.param['pixel_y'])
        self.surface.blit(self.image, self.rect)
        # for x in range(0, 11):
        #     for y in range(0, 23):
        #         self.update_coordinate(x, y)
        #         self.rect.center = (
        #             self.param['pixel_x'], self.param['pixel_y'])
        #         self.surface.blit(self.image, self.rect)
