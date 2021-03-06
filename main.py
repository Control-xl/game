import pygame
import sys
import game_functions as gf
import threading
from map import Map
from settings import Settings
from hero import Hero
from pause_menu import PauseMenu
from monster import MonsterBall
from monster import MonsterPlane
from state_display import StateDisplay
from weapon import Weapon, Bullet
from tool import Tool
from menu import Menu


if __name__ == '__main__':
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), 0, 0)
    menu = Menu(screen, settings)
    map_ = Map(screen, settings)
    hero = Hero(screen, map_, settings)
    # tool = Tool(screen, settings, "food", (600, 700))
    # tool_list.append(tool)
    monster_list = []
    # monster_list.append(MonsterPlane(settings, screen))
    # monsterball = MonsterBall(settings, screen)
    clock = pygame.time.Clock()
    screen.fill(settings.bg_color)
    gf.play_bg_music("music/forest01_new.ogg", -1)
    while True:
        clock.tick(200)
        gf.check_events(settings, screen, hero, menu)
        if hero.blood <= 0:
            menu.occupy = True
        if menu.occupy == True :
            menu.update(hero, map_, monster_list)
            menu.blitme(hero)
            if hero.blood_cd < 5:
                hero.blood_cd += 5
        else:
            # hero.update(monster_list, tool_list)
            hero.update1_v2(monster_list, map_.tool_list)
            map_.update(hero, monster_list)
            hero.update2_v2(int(map_.monster_point[map_.cnt-1]))
            monster_to_del = []
            for monster in monster_list:
                monster.update(hero)
                if monster.blood <= 0:
                    monster_to_del.append(monster)
            for monster in monster_to_del:
                monster_list.remove(monster)
                hero.money += 10
            # monsterball.update(hero)
            # monsterplane.update(hero)
            screen.fill(settings.bg_color)
            hero.blitme()
            for monster in monster_list:
                monster.blitme()
            map_.blitme()
        pygame.display.update()