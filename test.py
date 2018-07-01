import pygame
from settings import Settings
image = pygame.image.load('images/laser/bullet.png')
rect = image.get_rect()
rect.top = 0
rect.left = 0
pygame.init()
settings = Settings()
screen = pygame.display.set_mode((rect.width, rect.height), 0, 0)
screen.fill(settings.bg_color)
screen.blit(image, rect)
pygame.display.update()
pygame.image.save(screen, 'images/laser/bg_bullet.png')
bg_image = pygame.image.load('images/laser/bg_bullet.png')
count = 0
for x in range(rect.right):
    for y in range(rect.bottom):
        image_color = image.get_at((x, y))
        screen_color = screen.get_at((x, y))
        bg_image_color = bg_image.get_at((x, y))
        if screen_color != bg_image_color:
            count += 1
        print(image_color, screen_color, bg_image_color, count)
while True:
    pass