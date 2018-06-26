import pygame
class Tool():
    def __init__(self, name, pos, screen, settings):
        self.screen = screen
        self.name = name
        self.image = pygame.image.load(name + '.jpg')
        self.rect = self.image.get_rect()
        self.centerx = pos[0]
        self.bottom = pos[1]

    def blitme(self):
        self.screen.blit(self.image, self.rect)