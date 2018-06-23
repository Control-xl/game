import pygame
from settings import Settings
class Weapon():
    def __init__(self, settings):
        self.settings = settings
        self.bullets = []
        self.sword = {
            "center": 0
            "radius": 0
        }
        self.fist = None
        self.weapon = settings.weapon["fist"]


class Bullet():
    def __init__(self, screen, pos, velocity):
        self.screen = screen
        self.rect = self.pygame.get_rect()
        self.rect.left = self.pos[0]
        self.rect.centery = self.pos[1]
        self.velocity = velocity
        self.x = float(self.rect.x)
    def update(self):
        self.x += self.velocity
    def draw_bullet(self):
        pass
