import logging
import math
import pygame

from config.gameparams import GameParams
from sprite.player import Player
from display.camera import Camera
from display.display import Display
from display.grid import Grid
from worldmap.worldtile import WorldTile, Tile
from engine.window.textbox import TextBox
from engine.interupt import Interupt

logger = logging.getLogger()

class Engine:
    def __init__(self):
        self.mouse_motion_pos = (0,0)
        self.mouse_btnup_pos = (0,0)
        self.mouse_btndwn_pos = (0,0)

        self.interupt = Interupt.EXIT

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

        self.windows = {
            'console' : TextBox(Display.Surface['main'], 0, 0, 140, 32)
        }

        self.windows_list = [
            'console'
        ]

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

    def set_interupt(self, i):
        '''# interrupts
            #  0x1 main text input'''
        self.interupt = i
