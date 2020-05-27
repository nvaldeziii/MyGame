import math


class Grid:
    ANGLE1 = -60
    ANGLE2 = 60

    def __init__(self, game_window, pygame_draw, game_parameters):
        self.draw = pygame_draw
        self.window = game_window
        self.game_parameters = game_parameters

        self.window_size = self.game_parameters.Window.Width
        self.grid_thickness = 32

    def get_point2(self, point, slope):
        dx = point[0] + self.window_size
        b = point[1] - slope * point[0]
        return (dx, slope * dx + b)

    def render(self):
        '''https://www.pygame.org/docs/ref/draw.html#pygame.draw.line'''
        line_thickness = 1
        color = (0, 255, 0)

        point = (0, 0)
        while point[1] < self.game_parameters.Window.Height * 2:
            point2 = self.get_point2(point, math.tan(Grid.ANGLE1))
            self.draw.line(self.window, color,  point, point2, line_thickness)
            point = (point[0], point[1] + self.grid_thickness)

        point = (0, -self.game_parameters.Window.Height)
        while point[1] < self.game_parameters.Window.Height:
            point2 = self.get_point2(point, math.tan(Grid.ANGLE2))
            self.draw.line(self.window, color,  point, point2, line_thickness)
            point = (point[0], point[1] + self.grid_thickness)

    def render_coordinates(self):
        pass

