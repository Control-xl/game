import pygame
class Weapon():
    def __init__(self, settings):
        self.settings = settings
        self.bullets = []
        self.sword = {
            "centerx": 0,
            "centery": 0,
            "radius": 0
        }
        self.fist = None
        # self.weapon = settings.weapon["fist"]


class Bullet():
    def __init__(self, screen, pos, velocity):
        self.screen = screen
        self.rect = pygame.Rect(1,1,10,10)
        self.rect.left = pos[0]
        self.rect.centery = pos[1]
        self.velocity = velocity
        self.x = float(self.rect.x)
    def update(self):
        self.x += self.velocity
    def blitme(self):
        pygame.draw.rect(self.screen, (0,0,0), self.rect)
