import logging
import pygame

from engine.engine import Engine
from display.display import Display
from display.grid import Grid

logger = logging.getLogger()


class DisplayRect:
    def __init__(self):
        xy = Grid.get_pixel_coordinates(6, 14)
        self.param = {
            'pixel_x': xy[0],
            'pixel_y': xy[1]
        }


class MapMakerEngine(Engine):
    def __init__(self):
        Engine.__init__(self)
        self.display_rect = DisplayRect()

    def redraw_screen(self, ):
        pygame.display.set_caption(f"fps: {str(self.clock.get_fps())}")

        Display.Surface['main'].fill((0, 0, 0))

        self.camera.update(self.display_rect)

        self.world_tile.draw_bg(self.camera)

        for group in [
            'humanoid',
            'debug'
        ]:
            Display.Group[group].update()
            for sprite in Display.Group[group]:
                self.camera.apply(sprite)

        self.world_tile.draw_fg(self.camera)

        self.grid.draw()
        pygame.display.update()

    def events_handler(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.grid.toggle_visibility()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_btndwn_pos = event.pos
            if event.button == 1:
                for tile in Display.Group['tile']:
                    if tile.hitbox.collidepoint(
                            self.mouse_btndwn_pos[0],
                            self.mouse_btndwn_pos[1]):
                        print(
                            f"tile clicked: {tile.param['x_coordinate']}, {tile.param['y_coordinate']}")
                        tile.image = pygame.image.load(
                            'assets/sprites/tile/floor/placeholder_02.png')
                        tile.update()
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_btnup_pos = event.pos
            if event.button == 3:
                for tile in Display.Group['tile']:
                    if tile.param['x_coordinate'] == 6 and tile.param['y_coordinate'] == 14:
                        tile.update_rect(self.camera.x, self.camera.y)
                        pygame.draw.rect(tile.surface, (0, 255, 0), (self.camera.x,self.camera.y, 10 ,10), 0)
                        pygame.draw.rect(tile.surface, (0, 255, 0), tile.rect, 0)
                        pygame.draw.rect(tile.surface, (0, 0, 0), tile.hitbox, 0)

        if event.type == pygame.MOUSEMOTION:
            self.mouse_motion_pos = event.pos

    def initialize_world(self):
        '''Draw the world tiles then the player'''
        self.world_tile.generate_area()

    def update_debug_obj(self):
        self.grid.debug_obj.update({
            'mouse': {
                'rt': self.mouse_motion_pos,
                'btn_dn': self.mouse_btndwn_pos,
                'btn_up': self.mouse_btnup_pos,
            },
            'world_tile': self.world_tile.debug_obj(),
            'camera': self.camera.debug_obj()
        })
