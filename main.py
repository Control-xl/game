import pygame
import game_functions as gf
import threading
from map import Map
from settings import Settings
from ship import Ship
from hero import Hero
from pause_menu import PauseMenu
from monster import MonsterBall
from monster import MonsterPlane
from state_display import StateDisplay
from weapon import Weapon
from weapon import Bullet

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

    monster_ball = MonsterBall(settings, screen)
    monster_plane = MonsterPlane(settings, screen)
    # pygame.image.save(screen, 'background.tga')
    # 初始化状态展示信息，之后根据英雄的状态变化
    state_display = StateDisplay(screen, settings)

    map1 = Map(screen, settings)
    # hero = Hero(screen, map1, settings)
    hero = Ship(settings, screen)
    pause_menu = PauseMenu(settings, screen)

    # gf.play_bg_music("music/b.mp3")
    clock = pygame.time.Clock()
    weapon = Weapon(settings)

    tmp1 = 1000
    tmp_c = 100
    tmp_i = pygame.image.load('images/laser/0.png')
    tmp_i1 = pygame.transform.rotate(tmp_i, 0)
    tmp_i2 = pygame.transform.scale(tmp_i, (65, 1000))
    tmp_ang = 0
    while True:
        #clock.tick(1000)
        bullet = Bullet(screen, [1000, 400], 0)
        if len(weapon.bullets) < 1:
            weapon.bullets.append(bullet)
        if tmp1 > 0:
            tmp1 -=1
        else:
            tmp_c -= 1
            tmp1 = 100
            tmp_ang += 5
            tmp_i1 = pygame.transform.rotate(tmp_i2, tmp_ang )


        gf.check_events(settings, screen, hero)
        if not settings.pause:
            monster_ball.update(weapon)
        hero.update()
        map1.update(hero)
        state_display.update(hero)


        gf.update_screen(settings, screen, background_pic,
                         hero, map1, state_display, pause_menu, monster_ball, monster_plane)

        for i in weapon.bullets:
            i.blitme()
        # monster_plane.fire((800,600))
        monster_plane.update(hero)
        screen.blit(tmp_i, (50, 50))
        # screen.blit(tmp_i1, (100, 100))
        # screen.blit(tmp_i2, (200, 50))
        pygame.display.flip()

#run()

