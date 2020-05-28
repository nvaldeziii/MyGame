import pygame
import logging

from gameparams import GameParams
from sprite import Sprite
from humanoid import Player
from grid import Grid
from worldtile import Tile
from engine import Engine
from display import Display

# temp
import math
#

pygame.init()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

pygame.display.set_caption("gamename")
clock = pygame.time.Clock()
grid = Grid()
tile = Tile(Display.Surface['main'])
engine = Engine()
engine.player = Player(Display.Surface['main'], x_coordinate=5, y_coordinate=5)


def redraw_bg():
    Display.Surface['main'].fill((0, 0, 0))
    tile.draw()


def mouse_listener(keys):
    if keys[0] == 1:
        if engine.player.param['ready']:
            pygame.draw.line(Display.Surface['main'], (0, 0, 255),
                             (engine.player.param['pixel_x'],
                              engine.player.param['pixel_y']),
                             engine.mouse_pos, 4
                             )
            pygame.display.update()
            movement = engine.player.player_move(engine.mouse_pos)
            engine.player.delta_xy_coordinate(movement[0], movement[1])

while True:
    # https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick
    clock.tick(60)

    pygame.display.set_caption(
        f"fps: {str(clock.get_fps())}, mouse: {engine.mouse_pos}")
    # pygame.time.delay(1000)
    # logging.debug(f"tick ({tick})")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                grid.toggle_visibility()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            logger.debug(f"Cliked on: {pos}")

        if event.type == pygame.MOUSEMOTION:
            engine.mouse_pos = event.pos

    redraw_bg()
    engine.player.draw()

    mouse_listener(pygame.mouse.get_pressed())

    grid.debug_obj.update({'player': engine.player.param})
    grid.debug_obj.update({'player_debug': engine.player.debug_obj})
    grid.draw()
    pygame.display.update()
