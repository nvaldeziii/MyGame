import logging
import math

from sprite import Sprite
from event_handler import MouseClick

logger = logging.getLogger()


class Humanoid(Sprite):
    def __init__(self, surface=None, x_coordinate=0, y_coordinate=0):
        Sprite.__init__(self, surface, x_coordinate, y_coordinate, w=64, h=64)


class Player(Humanoid):
    def __init__(self, surface=None, x_coordinate=0, y_coordinate=0):
        Humanoid.__init__(self, surface, x_coordinate, y_coordinate)

    def player_move(self, mouse_pos):
        angle = MouseClick.get_angle_from_player(
            (self.pixel_x, self.pixel_y), mouse_pos)
        logger.debug(f"Mouse Angle from player: {angle}")
        logger.debug(
            f"current coordinate: {self.x_coordinate},{self.y_coordinate}")
        if angle > -0.2 and angle < 0.35:
            logger.debug(
                f"Moving player Right: {self.x_coordinate+1},{self.y_coordinate}")
            return (1, 0)
        if angle > -1.2 and angle < -0.2:
            # if y is even and down, don't add to x
            x = 0 if self.y_coordinate % 2 == 0 else 1
            logger.debug(
                f"Moving player DownRight: {self.x_coordinate+x},{self.y_coordinate+1}")
            return (x, 1)
        if angle > -2 and angle < -1.2:
            logger.debug(
                f"Moving player Down: {self.x_coordinate},{self.y_coordinate+2}")
            return (0, 2)
        if angle > -2.8 and angle < -2:
            # if y is odd and down, don't subtract to x
            x = 0 if self.y_coordinate % 2 != 0 else -1
            logger.debug(
                f"Moving player DownLeft: {self.x_coordinate+x},{self.y_coordinate+1}")
            return (x, 1)
        if (angle >= -math.pi and angle < -2.8) or (angle > 2.9 and angle <= math.pi):
            logger.debug(
                f"Moving player Left: {self.x_coordinate-1},{self.y_coordinate}")
            return (-1, 0)
        if angle > 2 and angle < 2.9:
            # if y is odd, don't decrease x
            x = 0 if self.y_coordinate % 2 != 0 else -1
            logger.debug(
                f"Moving player UpLeft: {self.x_coordinate+x},{self.y_coordinate-1}")
            return (x, -1)
        if angle > 1 and angle < 2:
            logger.debug(
                f"Moving player UpLeft: {self.x_coordinate},{self.y_coordinate-1}")
            return (0, -2)
        if angle > 0.35 and angle < 1:
            # if y is even. don't increase x
            x = 0 if self.y_coordinate % 2 == 0 else 1
            logger.debug(
                f"Moving player UpRight: {self.x_coordinate+x},{self.y_coordinate-1}")
            return (x, -1)
        else:
            return (0, 0)
