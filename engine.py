import logging
import math

from humanoid import Player
from display import Display
from worldmap.worldtile import WorldTile, Tile
from camera import Camera

logger = logging.getLogger()


class Engine:
    Interaction = True

    def __init__(self):
        self.player = Player(
            Display.Surface['main'], 'sprites/character/player/warrior_m.png',
            x_coordinate=6, y_coordinate=14)
        self.mouse_pos = None

        self.world_tile = WorldTile(Display.Group['tile'], Display.Group['tile_fg'])
        self.camera = Camera(self.world_tile.screen_lenght_x * Tile.DEFAULT_WIDTH,
                             self.world_tile.screen_lenght_y * Tile.DEFAULT_HEIGHT)
