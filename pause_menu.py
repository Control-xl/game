import pygame

class PauseMenu():
    def __init__(self, settings):
        self.settings = settings
        self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
        self.