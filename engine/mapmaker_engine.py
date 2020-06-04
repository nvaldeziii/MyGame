import logging
import pygame

from engine.engine import Engine
from display.display import Display
from display.grid import Grid
from engine.interupt import Interupt

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

        self.mouse_tile = [0,0]

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

        for window in self.windows_list:
            self.windows[window].draw()

        pygame.display.update()

    def interupt_handler(self, event):
        if self.interupt == Interupt.CONSOLE_INPUT:
            re = self.windows['console'].handle_event(event)
            if re == Interupt.TEXTBOX_ENTER:
                print(self.windows['console'].text)
                self.windows['console'].text = ''
            elif re == Interupt.EXIT:
                self.interupt = Interupt.EXIT

    def events_handler(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if self.interupt !=0:
            self.interupt_handler(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.grid.toggle_visibility()
            if event.key == pygame.K_BACKQUOTE:
                self.set_interupt(Interupt.CONSOLE_INPUT)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_btndwn_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_btnup_pos = event.pos
            if event.button == 3:
                pass
                # for tile in Display.Group['tile']:
                #     if tile.param['x_coordinate'] == 6 and tile.param['y_coordinate'] == 14:
                #         tile.update_rect(self.camera.x, self.camera.y)
                #         pygame.draw.rect(tile.surface, (0, 255, 0), (self.camera.x,self.camera.y, 10 ,10), 0)
                #         pygame.draw.rect(tile.surface, (0, 255, 0), tile.rect, 0)
                #         pygame.draw.rect(tile.surface, (0, 0, 0), tile.hitbox, 0)

        if event.type == pygame.MOUSEMOTION:
            self.mouse_motion_pos = event.pos
            tile = self.check_sprite_collision('tile', self.mouse_motion_pos)
            if tile:
                self.mouse_tile = [tile.param['x_coordinate'], tile.param['y_coordinate']]

    def check_sprite_collision(self, group,  pos):
        for sprite in Display.Group[group]:
            if sprite.hitbox.collidepoint(
                    self.mouse_motion_pos[0],
                    self.mouse_motion_pos[1]):
                return sprite
        return None

    def initialize_world(self):
        '''Draw the world tiles then the player'''
        self.world_tile.generate_area()

    def update_debug_obj(self):
        self.grid.debug_obj.update({
            'mouse': {
                'rt': self.mouse_motion_pos,
                'btn_dn': self.mouse_btndwn_pos,
                'btn_up': self.mouse_btnup_pos,
                'mouse_tile': self.mouse_tile,
            },
            'world_tile': self.world_tile.debug_obj(),
            'camera': self.camera.debug_obj()
        })
