import math
import pygame

from display import Display
from gameparams import GameParams


class Grid:
    ANGLE1 = -0.4636476093997
    ANGLE2 = -1 * ANGLE1
    # ANGLE1 = -(1/4) * math.pi
    # ANGLE2 = -1 * ANGLE1
    # ANGLE1 = -(1/6) * math.pi
    # ANGLE2 = (1/6) * math.pi

    def __init__(self):
        self.surface = Display.Surface['grid']

        self.grid_thickness = 50

        self.visible = False
        self.show_coordinate = True

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
        font = pygame.font.Font('font/AnonymousPro-Regular.ttf', 12)
        for x_coordinate in range(0, 10):
            for y_coordinate in range(0, 10):
                (x, y) = Grid.get_pixel_coordinates(x_coordinate, y_coordinate)
                text = font.render(
                    f'{x_coordinate},{y_coordinate}', True, (0,
                                                             0, 255)
                    # f'{x},{y}/{x_coordinate},{y_coordinate}', True, (255,
                    #                                                  255, 255)
                )
                textRect = text.get_rect()
                textRect.center = (x, y)
                self.surface.blit(text, textRect)

    @staticmethod
    def get_pixel_coordinates(x_coordinate, y_coordinate):
        ORIGIN = (70, 40)
        SPACING = (100, 25)

        NO_OFFSET = (0, 0)
        EVEN_ROW_OFFSET = (50, 0)
        OFFSET = NO_OFFSET if y_coordinate % 2 == 0 else EVEN_ROW_OFFSET

        x = ORIGIN[0] + OFFSET[0] + (SPACING[0] * x_coordinate)
        y = ORIGIN[1] + OFFSET[1] + (SPACING[1] * y_coordinate)

        return (x, y)

    @staticmethod
    def get_pixel_distance(x1, y1, x2, y2):
        '''pixel coordinate x and y'''
        return math.sqrt(math.pow((x2 - x1), 2) + math.pow(y2-y1, 2))
