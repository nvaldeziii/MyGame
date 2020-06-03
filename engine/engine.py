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
        self.mouse_motion_pos = (0,0)
        self.mouse_btnup_pos = (0,0)
        self.mouse_btndwn_pos = (0,0)

        self.world_tile = WorldTile(
            Display.Group['tile'], Display.Group['tile_fg']
        )

        self.camera = Camera(
            GameParams.config['window']['resolution']['width'],
            GameParams.config['window']['resolution']['height']
        )

        self.clock = pygame.time.Clock()
        self.grid = Grid()

        self._init_fonts()

    def _init_fonts(self):
        Display.Font.update({
            'debug': pygame.font.Font('assets/font/AnonymousPro-Regular.ttf', 12)
        })

    def update_debug_obj(self):
        raise NotImplementedError()

    def initialize_world(self):
        raise NotImplementedError()

    def redraw_screen(self):
        raise NotImplementedError()

    def events_handler(self, event):
        raise NotImplementedError()
