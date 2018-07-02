import pygame
import sys
from settings import Settings
from map import Map

class Tool():
    def __init__(self, screen, settings, name, pos, life_time = 5000):
        self.screen = screen
        self.settings = settings
        self.name = name
        self.image = pygame.image.load("images/tools/" + name + '.png')
        self.bg_image = pygame.image.load("images/tools/bg_" + name + '.png')
        self.rect = self.image.get_rect()
        self.centerx = pos[0]
        self.rect.bottom = pos[1]
        self.rect.centerx = pos[0]
        self.life_time = life_time

    def blitme(self):
        self.rect.centerx = self.centerx - self.settings.left_border
        self.life_time -= 1
        if self.life_time > 500 or (self.life_time > 0 and self.life_time % 10 >= 5) :
            self.screen.blit(self.image, self.rect)


if __name__ == '__main__':
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), 0, 0)
    screen.fill(settings.bg_color)
    map_ = Map(screen, settings)
    tools = []
    tool = Tool(screen, settings, "food", (600, 700), )
    tools.append(tool)
    clock = pygame.time.Clock()
    while True:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(settings.bg_color)
        map_.blitme()
        i = len(tools)
        while i > 0 :
            i -= 1
            if tools[i].life_time < 0 : 
                tools.pop(i)
        for tool in tools:
            tool.blitme()

