import pygame
from sprite import Sprite
from grid import Grid
from display import Display


class WorldTile:
    def __init__(self, surface, sprite_group):
        self.surface = surface
        self.sprite_group = sprite_group
        self.mapinfo = MapInfo()
        self.topleft = [0, 0]
        self.screen_lenght_x = 10
        self.screen_lenght_y = 10
        self.pixel_x = 0
        self.pixel_y = 0

    def debug_obj(self):
        return {
            'topleft': self.topleft
        }

    def change_topleft(self, topleft):
        self.topleft = topleft

    def generate_area(self):
        for x in range(self.topleft[0], self.screen_lenght_x):
            for y in range(self.topleft[1], self.screen_lenght_y):
                tile = Tile(self.surface, self.mapinfo.tiles[x][y]['img'])
                tile.update_coordinate(x, y)
                self.sprite_group.add(tile)
        self.sprite_group.update()

    def draw(self):
        Display.Surface['main'].blit(self.surface, (self.pixel_x, self.pixel_y))

class MapInfo:
    ONE_TILE = {
        'img': 'sprites/tile/sample.png'
    }

    def __init__(self, max_x=16):
        self.max_x = max_x
        self.tiles_total = self.max_x ** 2
        self.tiles = [[MapInfo.ONE_TILE] * self.max_x] * self.max_x


class Tile(Sprite):
    def __init__(self, surface, image):
        self.tile_w = 100
        self.tile_h = 50
        Sprite.__init__(self, surface, image, w=self.tile_w, h=self.tile_h)

    def render_coordinates(self):
        text = Display.Font['debug'].render(
            f"{self.param['x_coordinate']},{self.param['y_coordinate']}", True, (0, 0, 255))
        self.surface.blit(text, self.rect)

    def update(self):
        self.rect.center = (
            self.param['pixel_x'], self.param['pixel_y'])
        self.surface.blit(self.image, self.rect)
        self.render_coordinates()
