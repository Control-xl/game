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
from weapon import Weapon
from weapon import Bullet

if __name__ == '__main__':
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), 0, 0)
    map_ = Map(screen, settings)
    tools = []
    hero = Hero(screen, map_, tools, settings)
    monster_list = []
    monster_list.append(MonsterPlane(settings, screen))
    # monsterball = MonsterBall(settings, screen)
    clock = pygame.time.Clock()
    while True:
        clock.tick(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    hero.fire_magicing = True
                # if event.key == pygame.K_l:
                #     hero.get_hurt(settings.hero_direction["right"])
                if event.key == pygame.K_j:
                    hero.attacking = True
                if event.key == pygame.K_w:
                    hero.jumping = True
                if event.key == pygame.K_a:
                    hero.moving_left = True
                if event.key == pygame.K_d:
                    hero.moving_right = True
                if event.key == pygame.K_s:
                    hero.squating = False
                if event.key == pygame.K_0:
                    hero.change_weapon()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_k:
                    hero.fire_magicing = False
                if event.key == pygame.K_a:
                    hero.moving_left = False
                if event.key == pygame.K_d:
                    hero.moving_right = False
                if event.key == pygame.K_s:
                    hero.squating = False
        hero.update(monster_list)
        map_.update(hero, monster_list)
        monster_to_del = []
        for monster in monster_list:
            monster.update(hero)
            if monster.blood <= 0:
                monster_to_del.append(monster)

        for monster in monster_to_del:
            monster_list.remove(monster)
        # monsterball.update(hero)
        # monsterplane.update(hero)
        screen.fill(settings.bg_color)
        hero.blitme()
        for monster in monster_list:
            monster.blitme()
        map_.blitme()
        pygame.display.update()