import pygame
import json

from grid import Grid
from display import Display
from worldmap.tile import Tile
from worldmap.map_reader import MapReader


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

        self.map_id = self.get_map_id()

    def get_map_id(self):
        with open('worldmap/img_id.json', "r") as map_id:
            return json.loads(map_id.read())

    def debug_obj(self):
        return {
            'topleft': self.topleft,
            'center_coord': self.center_coord,
        }

    def generate_area(self):
        # for x in range(self.topleft[0], self.screen_lenght_x):
        #     for y in range(self.topleft[1], self.screen_lenght_y):
        #         tile = Tile(self.surface, self.mapinfo.tiles_info[x][y]['img'])
        #         tile.update_coordinate(x, y)
        #         self.sprite_group.add(tile)

        for i, tiledata in enumerate(self.mapinfo.tiles_info, 1):
            percent = (i / len(self.mapinfo.tiles_info)) * 100
            print(f"rendering tile: {percent}")
            tile_id = tiledata[0]
            tile_state = tiledata[1]
            tile_x_coord = tiledata[2]
            tile_y_coord = tiledata[3]


            image = self.map_id[f'{tile_id:04x}{tile_state:x}']
            tile = Tile(self.surface, image)

            tile.update_coordinate(tile_x_coord, tile_y_coord)
            self.sprite_group.add(tile)

        self.sprite_group.update()

    def draw(self, camera):
        Display.Surface['main'].blit(self.surface, (camera.x, camera.y))


class MapInfo:

    # ONE_TILE = {
    #     'img': 'sprites/tile/floor/placeholder_01.png'
    # }

    def __init__(self, max_x=80):
        self.max_x = max_x
        self.map_px_dimention = (
            self.max_x * Tile.DEFAULT_WIDTH, self.max_x * Tile.DEFAULT_HEIGHT)
        self.tiles_total = self.max_x ** 2
        # self.tiles_info = [[MapInfo.ONE_TILE] * self.max_x] * self.max_x

        mapreader = MapReader('map.bin')
        self.tiles_info = mapreader.data

        # for x in range(0, self.max_x):
        #     for y in range(0, self.max_x):
        #         self.tiles_info.append(
        #             [0, 0, 0, x, y]
        #         )
