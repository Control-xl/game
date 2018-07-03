import pygame
import sys
import math
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

def deal_image_1():
    pygame.init()
    settings = Settings()
    red_image_path = 'images/heart.ico'
    blue_image_path = 'images/blue_heart.png'
    blue_image = pygame.image.load(red_image_path)
    rect = blue_image.get_rect()
    screen = pygame.display.set_mode((rect.width, rect.height), 0, 0)
    for x in range(rect.right):
        for y in range(rect.bottom):
            (r, g, b, alpha) = blue_image.get_at((x, y))
            if r > 120 and b < 100 and g < 100:
                blue_image.set_at((x, y), (b, g, r, alpha))
    pygame.image.save(blue_image, blue_image_path)

def draw_circle():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((500, 500), 0, 0)
    screen.fill(settings.bg_color)
    pygame.draw.arc(screen, (255, 0, 0), (10,10,10, 10), 0, math.pi, 5) 
    #arc(Surface, color, Rect, start_angle, stop_angle, width=1) -> Rect
    pygame.display.update()
    i = 0
    while True:
        i += 1
        if i > 360:
            i = 1
        screen.fill(settings.bg_color)
        pygame.draw.arc(screen, (255, 0, 0), (50, 100, 100, 100), 0, (i/180) * math.pi, 1) 
        #arc(Surface, color, Rect, start_angle, stop_angle, width=1) -> Rect
        pygame.display.update()
    sys.exit()

if __name__ == '__main__':
    draw_circle()