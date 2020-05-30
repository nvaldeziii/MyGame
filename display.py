import pygame
from gameparams import GameParams


class Display:
    Font = {
        'debug' : None
    }

    Surface = {
        'main': pygame.display.set_mode(GameParams.Window.get_tuple_size()),
        'tile': None,
        'grid': pygame.Surface(GameParams.Window.get_tuple_size(), pygame.SRCALPHA, 32)
    }
    Surface['grid'] = Surface['grid'].convert_alpha()

    Group = {
        'tile': pygame.sprite.Group(),
        'humanoid': pygame.sprite.Group(),
        'debug': pygame.sprite.Group(),
    }
