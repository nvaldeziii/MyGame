import pygame
from sprite import Sprite
from grid import Grid
from display import Display


class WorldTile:
    def __init__(self, surface, sprite_group):
        self.mapinfo = MapInfo()
        self.surface = pygame.Surface(self.mapinfo.map_px_dimention)
        self.sprite_group = sprite_group
        self.topleft = [0, 0]
        self.center_coord = [6, 14]
        self.screen_lenght_x = 14
        self.screen_lenght_y = 28
        self.pixel_x = 0
        self.pixel_y = 0

    def debug_obj(self):
        return {
            'topleft': self.topleft,
            'center_coord': self.center_coord,
        }

    def generate_area(self):
        for x in range(self.topleft[0], self.screen_lenght_x):
            for y in range(self.topleft[1], self.screen_lenght_y):
                tile = Tile(self.surface, self.mapinfo.tiles[x][y]['img'])
                tile.update_coordinate(x, y)
                self.sprite_group.add(tile)
        self.sprite_group.update()

    def draw(self, camera):
        Display.Surface['main'].blit(self.surface, (camera.x, camera.y))


class MapInfo:
    ONE_TILE = {
        'img': 'sprites/tile/sample.png'
    }

    def __init__(self, max_x=80):
        self.max_x = max_x
        self.map_px_dimention = (self.max_x * Tile.DEFAULT_WIDTH, self.max_x * Tile.DEFAULT_HEIGHT)
        self.tiles_total = self.max_x ** 2
        self.tiles = [[MapInfo.ONE_TILE] * self.max_x] * self.max_x


class Tile(Sprite):
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 50
    def __init__(self, surface, image):
        self.tile_w = 100
        self.tile_h = 50
        Sprite.__init__(self, surface, image, w=self.tile_w, h=self.tile_h)

    def render_coordinates(self):
        text = Display.Font['debug'].render(
            f"{self.param['x_coordinate']},{self.param['y_coordinate']}", True, (0, 0, 255))
        text_rect = text.get_rect()
        text_rect.center = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])
        self.surface.blit(text, text_rect)

    def update(self):
        self.rect.center = (
            self.param['pixel_x'], self.param['pixel_y'])
        self.surface.blit(self.image, self.rect)
        self.render_coordinates()
