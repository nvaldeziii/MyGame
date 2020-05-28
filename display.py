import pygame
from gameparams import GameParams


class Display:
    game_parameters = GameParams()

    Surface = {
        'main': pygame.display.set_mode(GameParams.Window.get_tuple_size()),
        'grid': pygame.Surface(GameParams.Window.get_tuple_size(), pygame.SRCALPHA, 32)
    }

    Surface['grid'] = Surface['grid'].convert_alpha()
