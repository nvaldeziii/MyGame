import logging
import math
import pygame

from config.gameparams import GameParams
from sprite.player import Player
from display.camera import Camera
from display.display import Display
from display.grid import Grid
from worldmap.worldtile import WorldTile, Tile

logger = logging.getLogger()


class Engine:
    def __init__(self):
        self.mouse_pos = None

        self.world_tile = WorldTile(
            Display.Group['tile'], Display.Group['tile_fg'])

        self.camera = Camera(self.world_tile.screen_lenght_x * Tile.DEFAULT_WIDTH,
                             self.world_tile.screen_lenght_y * Tile.DEFAULT_HEIGHT)

        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self._init_fonts()

    def _init_fonts(self):
        Display.Font.update({
            'debug': pygame.font.Font('assets/font/AnonymousPro-Regular.ttf', 12)
        })

    def update_debug_obj(self):
        self.grid.debug_obj.update({
            'mouse': {'pos': self.mouse_pos},
            'world_tile': self.world_tile.debug_obj(),
            'camera': self.camera.debug_obj()
        })

    def initialize_world(self):
        raise NotImplementedError()

    def redraw_screen(self):
        raise NotImplementedError()

    def events_handler(self, event):
        raise NotImplementedError()
