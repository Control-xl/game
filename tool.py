import pygame
class Tool():
    def __init__(self, name):
        self.name = name
        self.image = pygame.image.load(name + '.jpg')
        self.rect = self.image.get_rect()
        
