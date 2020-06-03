import pygame
import logging

from config.gameparams import GameParams
from sprite.sprite import Sprite
from display.grid import Grid
from engine.mapmaker_engine import MapMakerEngine
from display.display import Display


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


pygame.init()
pygame.display.set_caption("gamename")

engine = MapMakerEngine()


camera_movement_sensitivity = .05


def mouse_listener(keys):
    if keys[2] == 1:
        engine.display_rect.param['pixel_x'] -= (
            engine.mouse_motion_pos[0]-engine.mouse_btndwn_pos[0]) * camera_movement_sensitivity
        engine.display_rect.param['pixel_y'] -= (
            engine.mouse_motion_pos[1]-engine.mouse_btndwn_pos[1]) * camera_movement_sensitivity


if __name__ == '__main__':
    engine.initialize_world()
    while True:
        # https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick
        engine.clock.tick(GameParams.config['clock'])

        mouse_listener(pygame.mouse.get_pressed())
        for event in pygame.event.get():
            engine.events_handler(event)

        engine.update_debug_obj()

        engine.redraw_screen()
