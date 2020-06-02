import pygame
from config.gameparams import GameParams


class Display:
    Font = {
        'debug' : None
    }

    Surface = {
        'main': pygame.display.set_mode(GameParams.window_tuple),
        'grid': pygame.Surface(GameParams.window_tuple, pygame.SRCALPHA, 32)
    }
    Surface['grid'] = Surface['grid'].convert_alpha()

    Group = {
        'tile': pygame.sprite.Group(),
        'wall': pygame.sprite.Group(),
        'humanoid': pygame.sprite.Group(),
        'tile_fg': pygame.sprite.Group(),
        'debug': pygame.sprite.Group(),
    }
