import pygame
import logging

from gameparams import GameParams
from sprite import Sprite
from grid import Grid
from worldtile import Tile
from engine import Engine

# temp
import math
#

pygame.init()

game_parameters = GameParams()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

game_window = pygame.display.set_mode(game_parameters.Window.get_tuple_size())

pygame.display.set_caption("gamename")
clock = pygame.time.Clock()

player = Sprite(game_window, x_coordinate=5, y_coordinate=5)
grid = Grid(game_parameters)
tile = Tile(game_window)
engine = Engine()
engine.player = player


def redraw_bg():
    game_window.fill((0, 0, 0))
    tile.draw()


def mouse_listener(keys):
    if keys[0] == 1:
        if engine.player.ready:
            pygame.draw.line(game_window, (0, 0, 255),
                             (player.pixel_x, player.pixel_y), engine.mouse_pos, 4)
            pygame.display.update()
            movement = engine.calculate_movement(engine.mouse_pos)
            player.delta_xy_coordinate(movement[0], movement[1])


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
    player.draw()

    mouse_listener(pygame.mouse.get_pressed())

    grid.draw(game_window)
    pygame.display.update()
