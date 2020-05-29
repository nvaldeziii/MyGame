import logging
import math
import pygame

from sprite import Sprite
from event_handler import MouseClick
from grid import Grid, MouseAngle

logger = logging.getLogger()


class Humanoid(Sprite):
    def __init__(self, surface, image, x_coordinate=0, y_coordinate=0):
        Sprite.__init__(self, surface,  image, x_coordinate=x_coordinate,
                        y_coordinate=y_coordinate, w=32, h=32)
        self.velocity = 2
        self.moving = False

        self.debug_obj = {
            'moving': 0,
            'vector': 0,
            'final_position': 0,
            'MouseTheta': 0
        }


class Player(Humanoid):
    def __init__(self, surface, image, x_coordinate=0, y_coordinate=0):
        Humanoid.__init__(self, surface, image,
                          x_coordinate=x_coordinate, y_coordinate=y_coordinate)

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
        self.surface.blit(
            self.image, self.rect,
            (33, 71, 32, 36)
        )

        # pygame.draw.rect(self.surface, (255, 0, 0), self.rect)

        if vector == final_position:
            self.moving = False
            self.param['ready'] = True
        self.param['pixel_x'] = vector[0]
        self.param['pixel_y'] = vector[1]

    def get_drawpoint(self):
        self.param['old_coordinate'] = (
            self.param['pixel_x'], self.param['pixel_y'])
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
        self.debug_obj.update({'MouseTheta': angle})

        if MouseAngle.RIGHT[0] > angle and angle > MouseAngle.RIGHT[1]:
            logger.debug(
                f"Moving player Right: {self.param['x_coordinate']+1},{self.param['y_coordinate']}")
            return (1, 0)
        elif MouseAngle.DOWN_RIGHT[0] < angle and angle < MouseAngle.DOWN_RIGHT[1]:
            # if y is even and down, don't add to x
            x = 0 if self.param['y_coordinate'] % 2 == 0 else 1
            logger.debug(
                f"Moving player DownRight: {self.param['x_coordinate']+x},{self.param['y_coordinate']+1}")
            return (x, 1)
        elif MouseAngle.DOWN[0] < angle and angle < MouseAngle.DOWN[1]:
            logger.debug(
                f"Moving player Down: {self.param['x_coordinate']},{self.param['y_coordinate']+2}")
            return (0, 2)
        elif MouseAngle.DOWN_LEFT[0] < angle and angle < MouseAngle.DOWN_LEFT[1]:
            # if y is odd and down, don't subtract to x
            x = 0 if self.param['y_coordinate'] % 2 != 0 else -1
            logger.debug(
                f"Moving player DownLeft: {self.param['x_coordinate']+x},{self.param['y_coordinate']+1}")
            return (x, 1)
        elif ((MouseAngle.LEFT[2] <= angle and angle < MouseAngle.LEFT[3])
              or (MouseAngle.LEFT[0] >= angle and angle > MouseAngle.LEFT[1])):
            logger.debug(
                f"Moving player Left: {self.param['x_coordinate']-1},{self.param['y_coordinate']}")
            return (-1, 0)
        elif MouseAngle.UP_LEFT[0] > angle and angle > MouseAngle.UP_LEFT[1]:
            # if y is odd, don't decrease x
            x = 0 if self.param['y_coordinate'] % 2 != 0 else -1
            logger.debug(
                f"Moving player UpLeft: {self.param['x_coordinate']+x},{self.param['y_coordinate']-1}")
            return (x, -1)
        elif MouseAngle.UP[0] > angle and angle > MouseAngle.UP[1]:
            logger.debug(
                f"Moving player Up: {self.param['x_coordinate']},{self.param['y_coordinate']-1}")
            return (0, -2)
        elif MouseAngle.UP_RIGHT[0] > angle and angle > MouseAngle.UP_RIGHT[1]:
            # if y is even. don't increase x
            x = 0 if self.param['y_coordinate'] % 2 == 0 else 1
            logger.debug(
                f"Moving player UpRight: {self.param['x_coordinate']+x},{self.param['y_coordinate']-1}")
            return (x, -1)
        else:
            logger.debug(
                f"Direction out of range: angle({angle})")
            return (0, 0)
