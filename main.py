import pygame
import logging

from config.gameparams import GameParams
from sprite.sprite import Sprite
from display.grid import Grid
from engine.game_engine import GameEngine
from display.display import Display


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


pygame.init()
pygame.display.set_caption("gamename")

engine = GameEngine()


def mouse_listener(keys):
    if keys[0] == 1:
        if engine.player.param['ready']:
            # pygame.display.update()
            if Grid.get_pixel_distance(
                engine.mouse_pos[0], engine.mouse_pos[1],
                engine.player.perma_px[0], engine.player.perma_px[1]
            ) > GameParams.config['player']['minimun_mouse_distance']:
                engine.player.move_by_mouse(engine.mouse_pos)
                engine.camera.update_tile_offset(engine.player)


if __name__ == '__main__':
    engine.initialize_world()
    while True:
        # https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick
        engine.clock.tick(GameParams.config['clock'])

        for event in pygame.event.get():
            engine.events_handler(event)

        mouse_listener(pygame.mouse.get_pressed())

        engine.update_debug_obj()

        engine.redraw_screen()
