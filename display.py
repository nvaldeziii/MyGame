import pygame
from gameparams import GameParams


class Display:
    Surface = {
        'tile': pygame.display.set_mode(GameParams.Window.get_tuple_size()),
        'main': pygame.display.set_mode(GameParams.Window.get_tuple_size()),
        'grid': pygame.Surface(GameParams.Window.get_tuple_size(), pygame.SRCALPHA, 32)
    }
    Surface['grid'] = Surface['grid'].convert_alpha()

    Group = {
        'tile': pygame.sprite.Group(),
        'humanoid': pygame.sprite.Group(),
        'debug': pygame.sprite.Group(),
    }
