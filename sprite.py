import pygame
from grid import Grid


class Sprite:
    def __init__(self, surface=None, x_coordinate=0, y_coordinate=0, w=64, h=64):
        self.surface = surface
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.w = w
        self.h = h
        self.get_drawpoint()
        self.ready = True

    def get_drawpoint(self):
        (self.pixel_x, self.pixel_y) = Grid.get_pixel_coordinates(
            self.x_coordinate, self.y_coordinate)

    def draw(self):
        pygame.draw.rect(self.surface, (255, 0, 0), (
            self.pixel_x - (self.w/2),
            self.pixel_y - self.h,
            self.w,
            self.h
        ))
        # pygame.draw.rect(self.surface, (255, 0, 0), (
        #     self.pixel_x - (self.w/2),
        #     self.pixel_y - self.h,
        #     self.w,
        #     self.h
        # ))

    def update_coordinate(self, x_coordinate, y_coordinate):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.get_drawpoint()

    def delta_xy_coordinate(self, x_coordinate, y_coordinate):
        self.x_coordinate += x_coordinate
        self.y_coordinate += y_coordinate
        self.get_drawpoint()
        self.animate_latidude_movement()

    def delta_x_coordinate(self, x_coordinate):
        self.x_coordinate += x_coordinate
        self.get_drawpoint()
        self.animate_latidude_movement()

    def delta_y_coordinate(self, y_coordinate):
        self.y_coordinate += y_coordinate
        self.get_drawpoint()

    # move to specialized class
    def animate_latidude_movement(self):
        self.ready = False
        pygame.time.wait(200)
        self.ready = True
