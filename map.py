import pygame
import game_functions as gf

class Map():

    def __init__(self, screen, settings):
        """初始化地图"""
        self.screen = screen
        self.settings = settings
        #初始化地图（为存档读档作准备）

        # self.left_border = settings.left_border
        # self.right_border = settings.right_border

        self.shape = [700 for i in range(1000)]

        for i in range(500):
            self.shape.append(600)
        for i in range(10000):
            self.shape.append(750)


    def update(self, hero, monster_list):
        """根据英雄位置和怪物更新地图信息"""

        velocityx = hero.velocityx
        rect = hero.rect

        # 如果有怪物，则锁屏
        if len(monster_list) > 0:
            self.settings.map_lock = True
        else:
            self.settings.map_lock = False

        # 再非锁屏状态下，地图随人物移动；锁屏状态下，地图不能随
        if not self.settings.map_lock:
            # 如果英雄向右移而且超过了屏幕的一一半位置wd
            if velocityx > 0 and\
                    rect.right >= self.settings.screen_width/2:
                # 且地图的右边界没有到达地图的最大位置
                if self.settings.right_border + self.settings.screen_width < self.settings.map_max:
                    self.settings.left_border += min(velocityx, self.settings.map_max - self.settings.right_border)
                    self.settings.right_border = self.settings.left_border + self.settings.screen_width

            # 如果英雄向左移而且到了屏幕左方1/10位置
            if velocityx < 0 and rect.left <= self.settings.screen_width/10:
                # 如果地图左边界没有到最左边的位置
                if self.settings.left_border > 0:
                    self.settings.left_border -= min(-velocityx, self.settings.left_border)
                    self.settings.right_border = self.settings.left_border + self.settings.screen_width


    def blitme(self):
        point_list = []
        for i in range(self.settings.screen_width):
            point_list.append((i, self.shape[i+self.settings.left_border]))
        # pygame.draw.lines(self.screen, (0, 0, 0), False, point_list, 3)
        pygame.draw.aalines(self.screen, (0, 0, 0), False, point_list, False)

    def gety(self, x):
        if x < 0 or x >= self.settings.map_max : 
            return 0
        elif x < self.settings.map_max :
            return self.shape[x]


