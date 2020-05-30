import copy
import logging
import math
import pygame

from display import Display
from gameparams import GameParams


logger = logging.getLogger()


class DirectionVector:
    RIGHT = [1, 0]
    UP_RIGHT = [1, -1]
    UP = [0, -2]
    UP_LEFT = [-1, -1]
    LEFT = [-1, 0]
    DOWN_LEFT = [-1, 1]
    DOWN = [0, 2]
    DOWN_RIGHT = [1, 1]
    CENTER = [0,0]


class MouseAngle:
    RIGHT = [0.39269908169, -0.39269908169]
    UP_RIGHT = [1.1780972451, 0.39269908169]
    UP = [1.96349540849, 1.1780972451]
    UP_LEFT = [2.74889357189, 1.96349540849]
    LEFT = [math.pi, 2.74889357189, -math.pi, -2.74889357189]
    DOWN_LEFT = [-2.74889357189, -1.96349540849]
    DOWN = [-1.96349540849, -1.1780972451]
    DOWN_RIGHT = [-1.1780972451, -0.39269908169]


class Grid:
    ANGLE1 = -0.4636476093997
    ANGLE2 = -1 * ANGLE1
    ORIGIN = [70,40]

    def __init__(self):
        self.surface = Display.Surface['grid']

        self.grid_thickness = 50
        self.dimention = (11, 23)
        self.visible = False
        self.show_coordinate = False
        self.debug_obj = {}

        self.test = 0

    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self._render()
            if self.show_coordinate:
                self._render_coordinates()

    def draw(self):
        if self.visible:
            Display.Surface['main'].blit(self.surface, (0, 0))
            if len(self.debug_obj) > 0:
                self._render_debug(self.debug_obj)

    def _get_point2(self, point, slope):
        dx = point[0] + GameParams.Window.Width
        b = point[1] - slope * point[0]
        return (dx, slope * dx + b)

    def _render(self):
        '''https://www.pygame.org/docs/ref/draw.html#pygame.draw.line'''
        line_thickness = 1
        color = (0, 255, 0)  # green

        point = (0, 0)
        while point[1] < GameParams.Window.Height * 2:
            point2 = self._get_point2(point, math.tan(Grid.ANGLE1))
            pygame.draw.line(self.surface, color,  point,
                             point2, line_thickness)
            point = (point[0], point[1] + self.grid_thickness)

        point = (0, -GameParams.Window.Height)
        while point[1] < GameParams.Window.Height:
            point2 = self._get_point2(point, math.tan(Grid.ANGLE2))
            pygame.draw.line(self.surface, color,  point,
                             point2, line_thickness)
            point = (point[0], point[1] + self.grid_thickness)

    def _render_coordinates(self):
        for x_coordinate in range(0, self.dimention[0]):
            for y_coordinate in range(0, self.dimention[1]):
                (x, y) = Grid.get_pixel_coordinates(x_coordinate, y_coordinate)
                text = Display.Font['debug'].render(
                    f'{x_coordinate},{y_coordinate}', True, (0,
                                                             0, 255)
                    # f'{x},{y}/{x_coordinate},{y_coordinate}', True, (255,
                    #                                                  255, 255)
                )
                textRect = text.get_rect()
                textRect.center = (x, y)
                self.surface.blit(text, textRect)

    def _render_debug(self, obj):
        x = 50
        y = 100
        padding = 15
        line = 1
        text_color = (0, 0, 0)
        bg_color = (255, 255, 255)
        for item in obj:
            text = Display.Font['debug'].render(f' {item} ', True, text_color, bg_color)
            textRect = text.get_rect()
            textRect.midleft = (x, y + (padding*line))
            self.surface.blit(text, textRect)
            line += 1
            for stats in obj[item]:
                text = Display.Font['debug'].render(
                    f' {stats}: {obj[item][stats]} ', True, text_color, bg_color)
                textRect = text.get_rect()
                textRect.midleft = (x+25, y + (padding*line))
                self.surface.blit(text, textRect)
                line += 1

    @staticmethod
    def get_pixel_coordinates(x_coordinate, y_coordinate):
        SPACING = (100, 25)

        NO_OFFSET = (0, 0)
        EVEN_ROW_OFFSET = (50, 0)
        OFFSET = NO_OFFSET if y_coordinate % 2 == 0 else EVEN_ROW_OFFSET

        x = Grid.ORIGIN[0] + OFFSET[0] + (SPACING[0] * x_coordinate)
        y = Grid.ORIGIN[1] + OFFSET[1] + (SPACING[1] * y_coordinate)

        return (x, y)

    @staticmethod
    def get_pixel_distance(x1, y1, x2, y2):
        '''pixel coordinate x and y'''
        return math.sqrt(math.pow((x2 - x1), 2) + math.pow(y2-y1, 2))

    @staticmethod
    def get_slope_angle(x1, y1, x2, y2):
        delta_x = x2 - x1
        delta_y = y2 - y1
        if delta_x == 0:
            angle = 0
            xdir = 0
            ydir = math.copysign(1, delta_y)
        else:
            angle = math.atan(delta_y / delta_x)
            xdir = math.copysign(1, delta_x)
            ydir = math.copysign(1, delta_y)
        return (angle, xdir, ydir)

    @staticmethod
    def get_y_intercept(y, m, x):
        return y-(m*x)

    @staticmethod
    def get_y_value(x1, y1, m, x3):
        b = Grid.get_y_intercept(y1, m, x1)
        return (m * x3) + b

    @staticmethod
    def get_movement_vector(x1, y1, x2, y2, velocity):
        plot = {}
        plot['angle'], plot['xdir'], plot['ydir'] = Grid.get_slope_angle(
            x1, y1, x2, y2)
        plot['m'] = math.tan(plot['angle'])

        if (x2 - x1) == 0:
            plot['y3'] = y1 + (.5 * velocity * plot['ydir'])
            plot['x3'] = x1

            if plot['ydir'] == -1:
                if plot['y3'] <= y2 - 1:
                    plot['y3'] = y2
            else:
                if plot['y3'] >= y2 - 1:
                    plot['y3'] = y2

        else:
            plot['x3'] = x1 + (velocity * plot['xdir'])

            if plot['xdir'] == 1:
                if plot['x3'] > x2 - 1:
                    plot['x3'] = x2
            else:
                if plot['x3'] < x2 + 1:
                    plot['x3'] = x2

            plot['y3'] = Grid.get_y_value(x1, y1, plot['m'], plot['x3'])

        # logger.debug(f"plot : {plot}")
        return (plot['x3'], plot['y3'])

    @staticmethod
    def get_direction_from_point_and_angle(angle):
        if MouseAngle.RIGHT[0] > angle and angle > MouseAngle.RIGHT[1]:
            return copy.deepcopy(DirectionVector.RIGHT)
        elif MouseAngle.DOWN_RIGHT[0] < angle and angle < MouseAngle.DOWN_RIGHT[1]:
            return copy.deepcopy(DirectionVector.DOWN_RIGHT)
        elif MouseAngle.DOWN[0] < angle and angle < MouseAngle.DOWN[1]:
            return copy.deepcopy(DirectionVector.DOWN)
        elif MouseAngle.DOWN_LEFT[0] < angle and angle < MouseAngle.DOWN_LEFT[1]:
            return copy.deepcopy(DirectionVector.DOWN_LEFT)
        elif ((MouseAngle.LEFT[2] <= angle and angle < MouseAngle.LEFT[3])
            or (MouseAngle.LEFT[0] >= angle and angle > MouseAngle.LEFT[1])):
            return copy.deepcopy(DirectionVector.LEFT)
        elif MouseAngle.UP_LEFT[0] > angle and angle > MouseAngle.UP_LEFT[1]:
            return copy.deepcopy(DirectionVector.UP_LEFT)
        elif MouseAngle.UP[0] > angle and angle > MouseAngle.UP[1]:
            return copy.deepcopy(DirectionVector.UP)
        elif MouseAngle.UP_RIGHT[0] > angle and angle > MouseAngle.UP_RIGHT[1]:
            return copy.deepcopy(DirectionVector.UP_RIGHT)
        else:
            return copy.deepcopy(DirectionVector.CENTER)
