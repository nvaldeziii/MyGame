from sprite import Sprite


class Tile(Sprite):
    DEFAULT_WIDTH = 100
    DEFAULT_HEIGHT = 50

    def __init__(self, surface, image):
        self.tile_w = 100
        self.tile_h = 50
        Sprite.__init__(self, surface, image, w=self.tile_w, h=self.tile_h)

    def render_coordinates(self):
        text = Display.Font['debug'].render(
            f"{self.param['x_coordinate']},{self.param['y_coordinate']}", True, (0, 0, 255))
        text_rect = text.get_rect()
        text_rect.center = Grid.get_pixel_coordinates(
            self.param['x_coordinate'], self.param['y_coordinate'])
        self.surface.blit(text, text_rect)

    def update(self, render_coordinate=False):
        self.rect.center = (
            self.param['pixel_x'], self.param['pixel_y'])
        self.surface.blit(self.image, self.rect)
        # self.render_coordinates()