import logging
import math

from humanoid import Player
from display import Display

logger = logging.getLogger()


class Engine:
    Interaction = True
    def __init__(self):
        self.player = Player(surface=Display.Surface['main'], x_coordinate=5, y_coordinate=5)
        self.mouse_pos = None
