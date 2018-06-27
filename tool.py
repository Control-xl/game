import pygame
from settings import Settings
from game_functions import transparent

class Tool():
    def __init__(self, name, pos, screen, settings):
        self.screen = screen
        self.settings = settings
        self.name = name
        self.image = pygame.image.load("tools/" + name + '.jpg')
        self.rect = self.image.get_rect()
        self.centerx = pos[0]
        self.bottom = pos[1]
        self.life_time = 10000

    def blitme(self):
        self.rect.centerx = self.centerx - self.settings.left_border
        self.life_time -= 1
        if self.life_time > 500 or self.life_time % 10 >= 5 :
            self.screen.blit(self.image, self.rect)


if __name__ == '__main__':
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), 0, 0)
    tools = []
