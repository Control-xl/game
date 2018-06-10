import pygame
import game_functions as gf
import threading
from map import Map
from settings import Settings
from hero import Ship


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

    __ = "github_test"
    #生成窗口，
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))


    pygame.display.set_caption("game")

    map1 = Map(screen, settings)
    hero = Ship(settings, screen)

    gf.play_bg_music("music/b.mp3")
    clock = pygame.time.Clock()

    while True:
        clock.tick(1000)
        gf.check_events(settings, screen, hero)
        hero.update()
        map1.update(hero)
        gf.update_screen(settings, screen, hero, map1)
        pygame.display.flip()
#run()

