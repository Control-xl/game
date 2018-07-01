import pygame
import sys
from settings import Settings
from game_functions import transparent
def image_calcul1():
    pygame.init()
    settings = Settings()
    jpg_image_path = 'images/tools/sword.jpg'
    png_image_path = 'images/tools/sword.png'
    bg_image_path = 'images/tools/bg_sword.png'
    jpg_image = pygame.image.load(jpg_image_path)
    rect = jpg_image.get_rect()
    rect.top = 0
    rect.left = 0
    screen = pygame.display.set_mode((rect.width, rect.height), 0, 0)
    jpg_image = jpg_image.convert_alpha()
    transparent(jpg_image)
    pygame.image.save(jpg_image, png_image_path)
    png_image = pygame.image.load(png_image_path)
    screen.fill(settings.bg_color)
    screen.blit(png_image, rect)
    pygame.display.update()
    pygame.image.save(screen, bg_image_path)
    bg_image = pygame.image.load(bg_image_path)
    count = 0
    for x in range(rect.right):
        for y in range(rect.bottom):
            png_image_color = png_image.get_at((x, y))
            screen_color = screen.get_at((x, y))
            bg_image_color = bg_image.get_at((x, y))
            if screen_color != bg_image_color:
                count += 1
            print(png_image_color, screen_color, bg_image_color, count)
    sys.exit()
def image_calcul2():
    pygame.init()
    settings = Settings()
    jpg_image_path = 'images/tools/food.png'
    png_image_path = 'images/tools/food.png'
    bg_image_path = 'images/tools/bg_food.png'
    jpg_image = pygame.image.load(png_image_path)
    rect = jpg_image.get_rect()
    rect.top = 0
    rect.left = 0
    screen = pygame.display.set_mode((rect.width, rect.height), 0, 0)
    jpg_image = jpg_image.convert_alpha()
    transparent(jpg_image)
    pygame.image.save(jpg_image, png_image_path)
    png_image = pygame.image.load(png_image_path)
    screen.fill(settings.bg_color)
    screen.blit(png_image, rect)
    pygame.display.update()
    pygame.image.save(screen, bg_image_path)
    bg_image = pygame.image.load(bg_image_path)
    count = 0
    for x in range(rect.right):
        for y in range(rect.bottom):
            png_image_color = png_image.get_at((x, y))
            screen_color = screen.get_at((x, y))
            bg_image_color = bg_image.get_at((x, y))
            if screen_color != bg_image_color:
                count += 1
            print(png_image_color, screen_color, bg_image_color, count)
    sys.exit()

image_calcul2()