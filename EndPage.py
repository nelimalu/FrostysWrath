import pygame
pygame.init()


def text_generator(text):
    tmp = ''
    for letter in text:
        tmp += letter
        # don't pause for spaces
        if letter != ' ':
            yield tmp

class DynamicText(object):
    def __init__(self, font, text, pos, autoreset=False):
        self.done = False
        self.font = font
        self.text = text
        self._gen = text_generator(self.text)
        self.pos = pos
        self.autoreset = autoreset
        self.update()

    def reset(self):
        self._gen = text_generator(self.text)
        self.done = False
        self.update()

    def update(self):
        if not self.done:
            try:
                self.rendered = self.font.render(next(self._gen), True, (255, 255, 0))
            except StopIteration:
                self.done = True
                if self.autoreset: self.reset()

    def draw(self, screen):
        screen.blit(self.rendered, self.pos)

