import logging
import pygame

from engine.engine import Engine

logger = logging.getLogger()


class MapMakerEngine(Engine):
    def __init__(self):
        Engine.__init__(self)

    def redraw_screen(self):
        pygame.display.set_caption(f"fps: {str(self.clock.get_fps())}")

        Display.Surface['main'].fill((0, 0, 0))

        self.camera.update(self.player)

        self.world_tile.draw_bg(self.camera)

        for group in [
            'humanoid',
            'debug'
        ]:
            Display.Group[group].update()
            for sprite in Display.Group[group]:
                self.camera.apply(sprite)

        self.world_tile.draw_fg(self.camera)

        # blue line from player to mouse
        if self.grid.visible:
            pygame.draw.line(Display.Surface['main'], (0, 0, 255),
                             (self.player.perma_px[0],
                              self.player.perma_px[1]),
                             self.mouse_pos, 4
                             )

        self.grid.draw()
        pygame.display.update()

    def events_handler(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.grid.toggle_visibility()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            logger.debug(f"Cliked on: {pos}")

        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos

    def initialize_world(self):
        '''Draw the world tiles then the player'''
        self.world_tile.generate_area()
        # Display.Group['humanoid'].add(self.player)