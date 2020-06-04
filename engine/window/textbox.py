import pygame

from display.display import Display
from engine.interupt import Interupt

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

class TextBox:
    '''https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
    '''

    def __init__(self, surface, x, y, w, h, text=''):
        self.surface = surface
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_ACTIVE
        self.text = text
        self.txt_surface = Display.Font['debug'].render(text, True, (0,255,0), (255,255,255))
        self.active = True
        self.interupt = 0x0001

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return Interupt.TEXTBOX_ENTER
                elif event.key == pygame.K_ESCAPE:
                    return Interupt.EXIT
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = Display.Font['debug'].render(self.text, True, (0,255,0), (255,255,255))
        return Interupt.CONTINUE

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        self.update()

        # Blit the text.
        self.surface.blit(self.txt_surface, (0, 0))
        # Blit the rect.
        pygame.draw.rect(self.surface, self.color, self.rect, 2)