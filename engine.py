import logging
import math

logger = logging.getLogger()


class Engine:
    def __init__(self):
        self.player = None
        self.mouse_pos = None

    def calculate_movement(self, mouse_pos):
        angle = MouseClick.get_angle_from_player(
            (self.player.pixel_x, self.player.pixel_y), mouse_pos)
        logger.debug(f"Mouse Angle from player: {angle}")
        logger.debug(
            f"current coordinate: {self.player.x_coordinate},{self.player.y_coordinate}")
        if angle > -0.2 and angle < 0.35:
            logger.debug(
                f"Moving player Right: {self.player.x_coordinate+1},{self.player.y_coordinate}")
            return (1, 0)
        if angle > -1.2 and angle < -0.2:
            # if y is even and down, don't add to x
            x = 0 if self.player.y_coordinate %2 == 0 else 1
            logger.debug(
                f"Moving player DownRight: {self.player.x_coordinate+x},{self.player.y_coordinate+1}")
            return (x, 1)
        if angle > -2 and angle < -1.2:
            logger.debug(
                f"Moving player Down: {self.player.x_coordinate},{self.player.y_coordinate+2}")
            return (0, 2)
        if angle > -2.8 and angle < -2:
            # if y is odd and down, don't subtract to x
            x = 0 if self.player.y_coordinate %2 != 0 else -1
            logger.debug(
                f"Moving player DownLeft: {self.player.x_coordinate+x},{self.player.y_coordinate+1}")
            return (x, 1)
        if (angle >= -math.pi and angle < -2.8) or (angle > 2.9 and angle <= math.pi):
            logger.debug(
                f"Moving player Left: {self.player.x_coordinate-1},{self.player.y_coordinate}")
            return (-1, 0)
        if angle > 2 and angle < 2.9:
            # if y is odd, don't decrease x
            x = 0 if self.player.y_coordinate %2 != 0 else -1
            logger.debug(
                f"Moving player UpLeft: {self.player.x_coordinate+x},{self.player.y_coordinate-1}")
            return (x, -1)
        if angle > 1 and angle < 2:
            logger.debug(
                f"Moving player UpLeft: {self.player.x_coordinate},{self.player.y_coordinate-1}")
            return (0, -2)
        if angle > 0.35 and angle < 1:
            # if y is even. don't increase x
            x = 0 if self.player.y_coordinate %2 == 0 else 1
            logger.debug(
                f"Moving player UpRight: {self.player.x_coordinate+x},{self.player.y_coordinate-1}")
            return (x, -1)
        else:
            return (0, 0)


class MouseClick:
    @staticmethod
    def get_angle_from_player(playerpos, mousepos):
        delta_x = mousepos[0] - playerpos[0]
        delta_y = playerpos[1] - mousepos[1]
        return math.atan2(delta_y, delta_x)
