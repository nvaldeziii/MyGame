import pygame
import logging

from config.gameparams import GameParams
from sprite.sprite import Sprite
from display.grid import Grid
from engine import Engine
from display.display import Display

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
    'debug': pygame.font.Font('assets/font/AnonymousPro-Regular.ttf', 12)
})


def init():
    engine.world_tile.generate_area()
    Display.Group['humanoid'].add(engine.player)


def redraw_screen():
    Display.Surface['main'].fill((0, 0, 0))

    engine.camera.update(engine.player)

    engine.world_tile.draw_bg(engine.camera)

    for group in [
        'humanoid',
        'debug'
    ]:
        Display.Group[group].update()
        for sprite in Display.Group[group]:
            engine.camera.apply(sprite)

    engine.world_tile.draw_fg(engine.camera)

    # blue line from player to mouse
    if grid.visible:
        pygame.draw.line(Display.Surface['main'], (0, 0, 255),
                                (engine.player.perma_px[0],
                                engine.player.perma_px[1]),
                                engine.mouse_pos, 4
                                )

    grid.draw()
    pygame.display.update()


def mouse_listener(keys):
    if keys[0] == 1:
        if engine.player.param['ready']:
            pygame.display.update()
            if Grid.get_pixel_distance(
                engine.mouse_pos[0], engine.mouse_pos[1],
                engine.player.perma_px[0], engine.player.perma_px[1]
            ) > 50:
                engine.player.move_by_mouse(engine.mouse_pos)
                engine.camera.update_tile_offset(engine.player)


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
                engine.world_tile.topleft = [
                    engine.world_tile.topleft[0] -
                    1, engine.world_tile.topleft[1] - 1
                ]
            if event.key == pygame.K_RIGHT:
                logger.debug(f"pressed K_RIGHT")
                engine.world_tile.topleft = [
                    engine.world_tile.topleft[0] +
                    1, engine.world_tile.topleft[1] + 1
                ]
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            logger.debug(f"Cliked on: {pos}")

        if event.type == pygame.MOUSEMOTION:
            engine.mouse_pos = event.pos

    mouse_listener(pygame.mouse.get_pressed())

    grid.debug_obj.update({
        'player': engine.player.param,
        'player_debug': engine.player.debug_obj(),
        'mouse': {'pos': engine.mouse_pos},
        'engine.world_tile': engine.world_tile.debug_obj(),
        'camera' : engine.camera.debug_obj()
    })

    redraw_screen()
