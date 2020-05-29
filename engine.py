import logging
import math

from humanoid import Player
from display import Display
from worldtile import WorldTile

logger = logging.getLogger()


class Engine:
    Interaction = True

    def __init__(self):
        self.player = Player(
            Display.Surface['main'], 'sprites/character/player/warrior_m.png',
            x_coordinate=6, y_coordinate=14)
        self.mouse_pos = None

        self.world_tile = WorldTile(Display.Surface['tile'], Display.Group['tile'])
