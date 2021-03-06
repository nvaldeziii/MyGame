import pygame
import json
import logging

from display.grid import Grid
from display.display import Display
from worldmap.tile import Tile
from worldmap.map_reader import MapReader

logger = logging.getLogger()


class WorldTile:
    def __init__(self, sprite_group, sprite_group_fg):
        self.mapinfo = MapInfo()

        self.surface = pygame.Surface(self.mapinfo.map_px_dimention)

        self.surface_fg = pygame.Surface(
            self.mapinfo.map_px_dimention, pygame.SRCALPHA, 32)
        self.surface_fg = self.surface_fg.convert_alpha()

        self.topleft = [0, 0]

        self.screen_lenght_x = 14
        self.screen_lenght_y = 28
        self.pixel_x = 0
        self.pixel_y = 0

        self.map_id = self.get_map_id()
        self.obj_id = self.get_obj_id()

        self.load_percent = 0

    def get_map_id(self):
        with open('assets/sprites/tile/img_id.json', "r") as map_id:
            return json.loads(map_id.read())

    def get_obj_id(self):
        with open('assets/sprites/tile/obj_id.json', "r") as map_id:
            return json.loads(map_id.read())

    def debug_obj(self):
        return {
            'topleft': self.topleft,
        }

    def generate_area(self):
        size = self.mapinfo.tiles.lenght * self.mapinfo.tiles.height
        count = 0
        for x in range(0, self.mapinfo.tiles.lenght):
            for y in range(0, self.mapinfo.tiles.height):
                self.load_percent = f'{count / size:.00%}'
                logger.debug(f"rendering tile: {self.load_percent}")
                count += 1

                tiledata = MapReader.tile_disector(
                    self.mapinfo.tiles.data[x][y], x, y)

                try:
                    map_id = self.map_id[f'{tiledata["tile_id"]}{tiledata["tile_state"]}']
                except KeyError as e:
                    map_id = self.map_id['00000']
                    logger.warning(f"error mapping tile ({x}, {y}): {e}")

                tile_image = map_id['img']
                tile_offset = map_id['offset']

                try:
                    if map_id['fg']:
                        obj_id = self.obj_id[f'{tiledata["tile_id"]}{tiledata["tile_state"]}']
                    else:
                        obj_id = self.obj_id[f'{tiledata["obj_id"]}{tiledata["obj_state"]}']
                    obj_image = obj_id['img']
                    obj_offset = obj_id['offset']

                    tile_obj = Tile(self.surface_fg, obj_image, obj_offset)
                    tile_obj.update_coordinate(y, x)
                    Display.Group['tile_fg'].add(tile_obj)
                except KeyError as e:
                    obj_id = self.obj_id['00000']
                    # logger.warning(f"error mapping object ({x}, {y}): {e}")

                tile = Tile(self.surface, tile_image, tile_offset)
                tile.update_coordinate(y, x)

                if tiledata['group'] == '0':
                    Display.Group['tile'].add(tile)
                elif tiledata['group'] == '1':
                    Display.Group['wall'].add(tile)

        Display.Group['tile'].update()
        Display.Group['wall'].update()
        Display.Group['tile_fg'].update()

    def draw(self, camera, surface):
        Display.Surface['main'].blit(surface, (camera.x, camera.y))

    def draw_bg(self, camera):
        self.draw(camera, self.surface)

    def draw_fg(self, camera):
        self.draw(camera, self.surface_fg)


class MapInfo:
    def __init__(self, max_x=80):
        self.max_x = max_x
        self.map_px_dimention = (
            self.max_x * Tile.DEFAULT_WIDTH, self.max_x * Tile.DEFAULT_HEIGHT)
        self.tiles_total = self.max_x ** 2

        self.tiles = MapReader()

        # self.tiles.from_binary('map.bin')
        self.tiles.from_json('worldmap/map.json')
