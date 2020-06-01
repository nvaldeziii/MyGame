import logging
import math
import pygame

from sprite import Sprite
from event_handler import MouseClick
from grid import Grid, MouseAngle, Direction
from display import Display

logger = logging.getLogger()


class Humanoid(Sprite):
    def __init__(self, surface, image, x_coordinate=0, y_coordinate=0):
        Sprite.__init__(self, surface,  image, x_coordinate=x_coordinate,
                        y_coordinate=y_coordinate, w=32, h=32)
        self.velocity = 2
        self.moving = False
        self.instance_name = 'none'

    def debug_obj(self):
        return {
            'moving': self.moving,
        }

    def move(self, x, y):
        self.last_vector = [x ,y]
        if not self.check_wall_collision(x, y):
            logger.debug(f"[{self.instance_name}] \
                ({self.param['x_coordinate'], self.param['y_coordinate']}) -> ({x}, {y})")
            self.param['x_coordinate'] = x
            self.param['y_coordinate'] = y

            self.get_drawpoint()
            self.param['ready'] = False
            self.moving = True

    def get_drawpoint(self):
        (self.param['x_final'], self.param['y_final']) = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])

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
        self.mouseTheta = 0
        self.instance_name = 'player'

    def debug_obj(self):
        return {
            'moving': self.moving,
            'mouseTheta': self.mouseTheta
        }

    def update(self):
        '''player moves for proof of concept'''
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

        if vector == final_position:
            self.moving = False
            self.param['ready'] = True
        self.param['pixel_x'] = vector[0]
        self.param['pixel_y'] = vector[1]

    def get_center_pixel(self, x, y):
        return (x - (self.param['w']/2), y - self.param['h'])

    def is_wall(self, wall, point):
        if wall.param['x_coordinate'] == point[0] and wall.param['y_coordinate'] == point[1]:
            logger.debug(
                f"wall coordinate: ({wall.param['x_coordinate']}, \
                {wall.param['y_coordinate']}) vs {point[0]},{point[1]}")
            return True
        return False

    def check_wall_collision(self, dx, dy):

        for wall in Display.Group['wall']:

            if self.is_wall(wall, (dx, dy)):
                return True

            self.coordinates_around[1]

            if self.direction == Direction.LEFT:
                if self.is_wall(wall, self.coordinates_around[1]) or self.is_wall(wall, self.coordinates_around[3]):
                    return True
            elif self.direction == Direction.RIGHT:
                if self.is_wall(wall, self.coordinates_around[5]) or self.is_wall(wall, self.coordinates_around[7]):
                    return True
            elif self.direction == Direction.UP:
                if self.is_wall(wall, self.coordinates_around[1]) or self.is_wall(wall, self.coordinates_around[5]):
                    return True
            elif self.direction == Direction.DOWN:
                if self.is_wall(wall, self.coordinates_around[3]) or self.is_wall(wall, self.coordinates_around[7]):
                    return True

        return False

    def move_by_mouse(self, mouse_pos):
        '''
            desc
        '''
        # mouse angle relative to player
        self.mouseTheta = MouseClick.get_angle_from_player(
            (self.perma_px[0], self.perma_px[1]),
            mouse_pos
        )

        # translate mouse angle to direction e.g. left, right, up, down
        self.direction = Grid.get_direction_from_point_and_angle(
            self.mouseTheta)

        # get every coordinate around
        self.coordinates_around = Grid.get_all_coordinates_around(
            [self.param['x_coordinate'], self.param['y_coordinate']]
        )

        self.last_vector = self.coordinates_around[self.direction]

        self.move(self.last_vector[0], self.last_vector[1])

        logger.debug(f"[PLAYER_ACTION] get_movement_from_mouse: direction:{self.direction}")
