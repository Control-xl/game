import pygame
import game_functions as gf
import threading
from map import Map
from settings import Settings
from ship import Ship
from hero import Hero
from pause_menu import PauseMenu
from monster import Monster
from state_display import StateDisplay
if __name__ == '__main__':
    #def run():

    """初始化参数"""
    # 获得设定
    settings = Settings()
    # 音乐播放初始化
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    # pygame初始化
    pygame.init()
    # 设置bgm音量
    pygame.mixer.music.set_volume(settings.volume)
    # 设置标题
    pygame.display.set_caption("game")
    # 生成窗口
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    # screen.fill(settings.bg_color)
    # pygame.image.save(screen, 'images/background.jpeg')
    background_pic = pygame.image.load('images/background.jpeg')
    background_pic.convert(screen)

    monster_test = Monster(settings, screen)


    # pygame.image.save(screen, 'background.tga')
    # 初始化状态展示信息，之后根据英雄的状态变化
    state_display = StateDisplay(screen, settings)

    map1 = Map(screen, settings)
    # hero = Hero(screen, map1, settings)
    hero = Ship(settings, screen)
    pause_menu = PauseMenu(settings, screen)

    # gf.play_bg_music("music/b.mp3")
    clock = pygame.time.Clock()

    while True:
        #clock.tick(1000)
        monster_test.update()

        gf.check_events(settings, screen, hero)
        # if settings.pause == False:
        hero.update()
        map1.update(hero)
        state_display.update(hero)

        gf.update_screen(settings, screen, background_pic,
                         hero, map1, state_display, pause_menu, monster_test)
        pygame.display.flip()

#run()

