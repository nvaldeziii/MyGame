import pygame
import logging

from gameparams import GameParams
from sprite import Sprite
from grid import Grid

pygame.init()

game_parameters = GameParams()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

game_window = pygame.display.set_mode(game_parameters.Window.get_tuple_size())

pygame.display.set_caption("gamename")
clock = pygame.time.Clock()

rect_box = Sprite(0, 50, 32, 32)
velocity = 5

grid = Grid(game_window, pygame.draw, game_parameters)

def redraw_bg():
    game_window.fill((0, 0, 0))

def check_key_press():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_TAB]:
        grid.render()
    if keys[pygame.K_LEFT]:
        rect_box.x -= velocity
    if keys[pygame.K_RIGHT]:
        rect_box.x += velocity
    if keys[pygame.K_UP]:
        rect_box.y -= velocity
    if keys[pygame.K_DOWN]:
        rect_box.y += velocity

while True:
    clock.tick(60)  # https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick

    pygame.display.set_caption(f"fps: {str(clock.get_fps())}")
    # pygame.time.delay(1000)
    # logging.debug(f"tick ({tick})")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


    redraw_bg()
    check_key_press()
    pygame.draw.rect(game_window, (255, 0, 0), (rect_box.x,
                                                rect_box.y, rect_box.w, rect_box.h))

    grid.render()
    pygame.display.update()
