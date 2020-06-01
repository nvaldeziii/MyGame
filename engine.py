import logging
import math

from config.gameparams import GameParams
from sprite.player import Player
from display.camera import Camera
from display.display import Display
from worldmap.worldtile import WorldTile, Tile

logger = logging.getLogger()
GameParams.init()

class Engine:
    Interaction = True

    def __init__(self):
        self.player = Player(
            Display.Surface['main'], 'assets/sprites/character/player/warrior_m.png',
            x_coordinate=6, y_coordinate=14)
        self.mouse_pos = None

        self.world_tile = WorldTile(Display.Group['tile'], Display.Group['tile_fg'])
        self.camera = Camera(self.world_tile.screen_lenght_x * Tile.DEFAULT_WIDTH,
                             self.world_tile.screen_lenght_y * Tile.DEFAULT_HEIGHT)
