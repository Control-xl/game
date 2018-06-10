import pygame
import sys
import threading

def check_keydown_events(event, settings, screen, hero):
    if event.key == pygame.K_RIGHT:
         # 右移
        hero.moving_right = True
    if event.key == pygame.K_LEFT:
        # left移
        hero.moving_left = True


def check_keyup_events(event, hero):
    if event.key == pygame.K_RIGHT:
        hero.moving_right = False
    if event.key == pygame.K_LEFT:
        hero.moving_left = False


def check_events(settings, screen, hero):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, hero)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, hero)


def update_screen(settings, screen, hero, map):
    screen.fill(settings.bg_color)
    hero.blitme()
    map.blitme()



def play_short_music(music_name,  volume = 0.1, loops = 0):
    """播放短效音乐，比如击中 等效果，建议以ogg结尾"""
    music = pygame.mixer.Sound(music_name)
    music.set_volume(volume)
    music.play(loops)


def play_bg_music(music_name, loops = -1):
    """播放背景音乐，MP3格式"""
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.play(loops)



