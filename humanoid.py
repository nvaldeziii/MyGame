import logging
import math
import pygame

from sprite import Sprite
from event_handler import MouseClick
from grid import Grid, MouseAngle, DirectionVector
from display import Display

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
    def __init__(self, surface, image, x_coordinate, y_coordinate):
        Humanoid.__init__(self, surface, image,
                          x_coordinate=x_coordinate, y_coordinate=y_coordinate)

        self.center_px = Grid.get_pixel_coordinates(x_coordinate, y_coordinate)

        self.perma_coord = (x_coordinate, y_coordinate)
        self.perma_px = Grid.get_pixel_coordinates(
            self.perma_coord[0], self.perma_coord[1])
        self.rect.midbottom = (self.perma_px[0], self.perma_px[1])

        self.last_vector = (0, 0)

    def update2(self):
        self.rect.midbottom = (self.center_px[0], self.center_px[1])
        self.surface.blit(
            self.image, self.rect,
            (33, 71, 32, 36)
        )

        self.moving = False
        self.param['ready'] = True

    def update(self):
        '''player moves for proof of concept,
           tile should move in next verion'''
        self.surface.blit(
            self.image, self.rect,
            (33, 71, 32, 36)
        )

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

        self.debug_obj.update({
            'moving': self.moving,
            'vector': vector,
            'final_position': final_position
        })

        if vector == final_position:
            self.moving = False
            self.param['ready'] = True
        self.param['pixel_x'] = vector[0]
        self.param['pixel_y'] = vector[1]

    def get_drawpoint(self):
        # self.param['old_coordinate'] = (
        #     self.param['pixel_x'], self.param['pixel_y'])
        (self.param['x_final'], self.param['y_final']) = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])

    def get_center_pixel(self, x, y):
        return (x - (self.param['w']/2), y - self.param['h'])

    def check_wall_collision(self, x, y):
        for wall in Display.Group['wall']:
            if wall.param['x_coordinate'] == x and wall.param['y_coordinate'] == y:
                logger.debug(
                    f"wall coordinate: ({wall.param['x_coordinate']},{wall.param['y_coordinate']}) vs {x},{y}")
                return True
        return False

    def delta_xy_coordinate(self, x_coordinate, y_coordinate):
        if not self.check_wall_collision(
                self.param['x_coordinate'] + x_coordinate,
                self.param['y_coordinate'] + y_coordinate):
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
                self.perma_px[0],
                self.perma_px[1]
            ),
            mouse_pos
        )
        self.debug_obj.update({'MouseTheta': angle})

        self.last_vector = Grid.get_direction_from_point_and_angle(angle)

        logger.debug(f"get_direction_from_point_and_angle: {self.last_vector}")
        if self.last_vector == DirectionVector.DOWN_RIGHT:
            self.last_vector[0] = 0 if self.param['y_coordinate'] % 2 == 0 else 1
        elif self.last_vector == DirectionVector.DOWN_LEFT:
            self.last_vector[0] = 0 if self.param['y_coordinate'] % 2 != 0 else -1
        elif self.last_vector == DirectionVector.UP_RIGHT:
            self.last_vector[0] = 0 if self.param['y_coordinate'] % 2 == 0 else 1
        elif self.last_vector == DirectionVector.UP_LEFT:
            self.last_vector[0] = 0 if self.param['y_coordinate'] % 2 != 0 else -1

        logger.debug(f"self.last_vector: {self.last_vector}")
        return self.last_vector
