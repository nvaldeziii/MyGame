import pygame
import logging

from gameparams import GameParams
from sprite import Sprite
from humanoid import Player
from grid import Grid
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
engine = Engine()

Display.Font.update({
    'debug': pygame.font.Font('font/AnonymousPro-Regular.ttf', 12)
})


def init():
    engine.world_tile.generate_area()
    Display.Group['humanoid'].add(engine.player)


def redraw_screen():
    Display.Surface['main'].fill((0, 0, 0))
    engine.world_tile.draw()
    for group in [
        'humanoid',
        'debug'
    ]:
        Display.Group[group].update()
    grid.draw()
    pygame.display.update()


def mouse_listener(keys):
    if keys[0] == 1:
        if engine.player.param['ready']:
            pygame.draw.line(Display.Surface['main'], (0, 0, 255),
                             (engine.player.param['pixel_x'],
                              engine.player.param['pixel_y']),
                             engine.mouse_pos, 4
                             )
            pygame.display.update()
            if Grid.get_pixel_distance(
                engine.mouse_pos[0], engine.mouse_pos[1],
                engine.player.param['pixel_x'], engine.player.param['pixel_y']
            ) > 50:
                movement = engine.player.player_move(engine.mouse_pos)
                engine.player.delta_xy_coordinate(movement[0], movement[1])


init()
while True:
    # https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick
    clock.tick(60)

    pygame.display.set_caption(
        f"fps: {str(clock.get_fps())}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                grid.toggle_visibility()
            if event.key == pygame.K_LEFT:
                logger.debug(f"pressed K_LEFT")
                # engine.world_tile.pixel_x += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            logger.debug(f"Cliked on: {pos}")

        if event.type == pygame.MOUSEMOTION:
            engine.mouse_pos = event.pos

    # key = pygame.key.get_pressed()
    # if key[pygame.K_RIGHT]:
    #     engine.world_tile.pixel_x += 1

    mouse_listener(pygame.mouse.get_pressed())

    grid.debug_obj.update({
        'player': engine.player.param,
        'player_debug': engine.player.debug_obj,
        'mouse': {'pos': engine.mouse_pos},
        'engine.world_tile': engine.world_tile.debug_obj()
    })

    redraw_screen()

