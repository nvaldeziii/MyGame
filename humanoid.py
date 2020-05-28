import logging
import math
import pygame

from sprite import Sprite
from event_handler import MouseClick
from grid import Grid

logger = logging.getLogger()


class Humanoid(Sprite):
    def __init__(self, surface=None, x_coordinate=0, y_coordinate=0):
        Sprite.__init__(self, surface, x_coordinate, y_coordinate, w=32, h=32)
        self.velocity = 1
        self.moving = False
        self.debug_obj = {}


class Player(Humanoid):
    def __init__(self, surface=None, x_coordinate=0, y_coordinate=0):
        Humanoid.__init__(self, surface, x_coordinate, y_coordinate)

    def draw(self):
        final_position = (self.param['x_final'], self.param['y_final'])
        vector = final_position
        if self.moving:
            vector = Grid.get_movement_vector(
                self.param['pixel_x'],
                self.param['pixel_y'],
                self.param['x_final'],
                self.param['y_final'],
                self.velocity
            )

            pygame.draw.line(self.surface, (255, 255, 0),
                             (self.param['old_coordinate'][0],
                              self.param['old_coordinate'][1]),
                             final_position, 5)

        self.debug_obj.update({
            'moving': self.moving,
            'vector': vector,
            'final_position': final_position
        })

        self.rect.midbottom = (vector[0], vector[1])
        pygame.draw.rect(self.surface, (255, 0, 0), self.rect)

        if vector == final_position:
                self.moving = False
                self.param['ready'] = True
        self.param['pixel_x'] = vector[0]
        self.param['pixel_y'] = vector[1]

    def get_drawpoint(self):
        self.param['old_coordinate'] = (self.param['pixel_x'], self.param['pixel_y'])
        (self.param['x_final'], self.param['y_final']) = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])

    def get_center_pixel(self, x, y):
        return (x - (self.param['w']/2), y - self.param['h'])

    def delta_xy_coordinate(self, x_coordinate, y_coordinate):
        self.param['x_coordinate'] += x_coordinate
        self.param['y_coordinate'] += y_coordinate
        self.get_drawpoint()
        self.param['ready'] = False
        self.moving = True
        # self.animate_latidude_movement()

    def animate_latidude_movement(self):
        self.param['ready'] = False
        pygame.time.wait(200)
        self.param['ready'] = True

    def player_move(self, mouse_pos):
        angle = MouseClick.get_angle_from_player(
            (self.param['pixel_x'], self.param['pixel_y']), mouse_pos)
        logger.debug(f"Mouse Angle from player: {angle}")
        logger.debug(
            f"current coordinate: {self.param['x_coordinate']},{self.param['y_coordinate']}")
        if angle > -0.2 and angle < 0.35:
            logger.debug(
                f"Moving player Right: {self.param['x_coordinate']+1},{self.param['y_coordinate']}")
            return (1, 0)
        if angle > -1.2 and angle < -0.2:
            # if y is even and down, don't add to x
            x = 0 if self.param['y_coordinate'] % 2 == 0 else 1
            logger.debug(
                f"Moving player DownRight: {self.param['x_coordinate']+x},{self.param['y_coordinate']+1}")
            return (x, 1)
        if angle > -2 and angle < -1.2:
            logger.debug(
                f"Moving player Down: {self.param['x_coordinate']},{self.param['y_coordinate']+2}")
            return (0, 2)
        if angle > -2.8 and angle < -2:
            # if y is odd and down, don't subtract to x
            x = 0 if self.param['y_coordinate'] % 2 != 0 else -1
            logger.debug(
                f"Moving player DownLeft: {self.param['x_coordinate']+x},{self.param['y_coordinate']+1}")
            return (x, 1)
        if (angle >= -math.pi and angle < -2.8) or (angle > 2.9 and angle <= math.pi):
            logger.debug(
                f"Moving player Left: {self.param['x_coordinate']-1},{self.param['y_coordinate']}")
            return (-1, 0)
        if angle > 2 and angle < 2.9:
            # if y is odd, don't decrease x
            x = 0 if self.param['y_coordinate'] % 2 != 0 else -1
            logger.debug(
                f"Moving player UpLeft: {self.param['x_coordinate']+x},{self.param['y_coordinate']-1}")
            return (x, -1)
        if angle > 1 and angle < 2:
            logger.debug(
                f"Moving player UpLeft: {self.param['x_coordinate']},{self.param['y_coordinate']-1}")
            return (0, -2)
        if angle > 0.35 and angle < 1:
            # if y is even. don't increase x
            x = 0 if self.param['y_coordinate'] % 2 == 0 else 1
            logger.debug(
                f"Moving player UpRight: {self.param['x_coordinate']+x},{self.param['y_coordinate']-1}")
            return (x, -1)
        else:
            return (0, 0)
