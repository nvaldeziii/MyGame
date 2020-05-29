import logging
import math
import pygame

from sprite import Sprite
from event_handler import MouseClick
from grid import Grid, MouseAngle, DirectionVector

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
        '''
            desc
        '''
        angle = MouseClick.get_angle_from_player(
            (
                self.param['pixel_x'],
                self.param['pixel_y']
            ),
            mouse_pos
        )
        self.debug_obj.update({'MouseTheta': angle})

        d_vect = Grid.get_direction_from_point_and_angle(angle)

        logger.debug(f"get_direction_from_point_and_angle: {d_vect}")
        if d_vect == DirectionVector.DOWN_RIGHT:
            d_vect[0] = 0 if self.param['y_coordinate'] % 2 == 0 else 1
        elif d_vect == DirectionVector.DOWN_LEFT:
            d_vect[0] = 0 if self.param['y_coordinate'] % 2 != 0 else -1
        elif d_vect == DirectionVector.UP_RIGHT:
            d_vect[0] = 0 if self.param['y_coordinate'] % 2 == 0 else 1
        elif d_vect == DirectionVector.UP_LEFT:
            d_vect[0] = 0 if self.param['y_coordinate'] % 2 != 0 else -1

        logger.debug(f"d_vect: {d_vect}")
        return d_vect
