import pygame
import monster
import game_functions as gf


class Map():

    def __init__(self, screen, settings):
        """初始化地图"""
        self.screen = screen
        self.settings = settings
        # 初始化地图（为存档读档作准备）

        # self.left_border = settings.left_border
        # self.right_border = settings.right_border

        self.shape = []

        self.cnt = 0
        # 第一只怪为
        self.monster_point = []
        self.monster_list = []

        for i in range(500):
            self.shape.append(500)
        # 飞机，依次为血量，攻击准备时间，蓄力时间，最大子弹数，x，y
        # 球，以此为保护圈血量，中心血量，保护圈数目，初始位置x，y， 保护转速，中心平移速度

        self.monster_point.append(600)
        self.monster_point.append(2300)

        # # map1，飞机， 长度1200
        # self.monster_list.append([monster.MonsterPlane(settings, screen, 1, 10000, 500, 1, 1000, 500)])
        # for i in range(1200):
        #     self.shape.append(700)
        # # 怪物出现点
        # self.monster_point.append(600)
        #
        # # 过渡段
        # for i in range(600):
        #     self.shape.append(600)
        # # 2300
        #
        # # map2，球
        # self.monster_list.append([monster.MonsterBall(settings, screen)])
        # for i in range(1200):
        #     self.shape.append(700)
        # self.monster_point.append(2600)
        #
        # # 过渡段
        # for i in range(600):
        #     self.shape.append(600)
        # # 4100


        # 3球
        self.monster_list.append([monster.MonsterBall(settings, screen, 1, 1, 1, 1000, 500, 0.1, 0.5)])
        for j in range(12):
            for i in range(50):
                self.shape.append(600)
            for i in range(50):
                self.shape.append(700)
        self.monster_point.append(4500)

        # 过渡段
        for i in range(600):
            self.shape.append(600)
        # 5900


        # # 4飞机 * 2
        # self.monster_list.append([monster.MonsterPlane(settings, screen, 2, 3000, 1000, 1, 1000, 200),
        #                           monster.MonsterPlane(settings, screen, 2, 10000, 1000, 10, 1000, 520)])
        # for i in range(1200):
        #     self.shape.append(700)
        # self.monster_point.append(6100)
        #
        # # 过渡段
        # for i in range(600):
        #     self.shape.append(600)
        # # 7700


        # 5球
        self.monster_list.append([monster.MonsterBall(settings, screen, 1, 10, 3, 1100, 500, 0.1, 0.01)])
        for i in range(1200):
            self.shape.append(700)
        self.monster_point.append(7900)

        # 过渡段
        for i in range(600):
            self.shape.append(600)
        # 9500

        # 6
        # 0-100
        for i in range(100):
            self.shape.append(700)
        # 100-200
        for i in range(100):
            self.shape.append(600)
        # 200-300
        for i in range(100):
            self.shape.append(700)
        # 300-400
        for i in range(100):
            self.shape.append(500)
        # 400-550
        for i in range(150):
            self.shape.append(self.settings.BOTTOM_NUM)
        # 550-650
        for i in range(100):
            self.shape.append(400)
        # 650-850
        for i in range(200):
            self.shape.append(self.settings.BOTTOM_NUM)
        # 850-950
        for i in range(100):
            self.shape.append(300)
        for i in range(250):
            self.shape.append(700)

        # 10700

        # map 7
        #self.monster_list.append([monster.MonsterPlane(settings, screen, 5, 5000, 300, 3, 1000, 300)])
        #self.monster_list.append([monster.MonsterBall(settings, screen, 1, 10, 5, 1100, 500, 0.1, 0.1)])
        for i in range(1200):
            self.shape.append(700)




        # for test
        # 怪物数量
        self.max_index = len(self.monster_list)

        # to del


        for i in range(1200):
            self.shape.append(400)

    def update(self, hero, monster_list):
        """根据英雄位置和怪物更新地图信息"""

        velocityx = hero.velocityx
        rect = hero.rect
        if self.cnt < self.max_index:
            if hero.x >= self.monster_point[self.cnt]:
                for monster in self.monster_list[self.cnt]:
                    monster_list.append(monster)
                self.cnt += 1

        # 如果有怪物，则锁屏
        if len(monster_list) > 0:
            self.settings.map_lock = True
        else:
            self.settings.map_lock = False

        # 如果掉下了坑，则移到英雄的位置
        # or hero.x + hero.rect.width > self.settings.right_border + 10
        if hero.x < self.settings.left_border :
            self.settings.left_border = max(hero.x - 100, 0)

        # 再非锁屏状态下，地图随人物移动；锁屏状态下，地图不能随
        if not self.settings.map_lock:
            # 如果英雄向右移而且超过了屏幕的三分之一位置，那么加速移动
            if velocityx > 0 and rect.right > self.settings.screen_width / 3:
                # 且地图的右边界没有到达地图的最大位置
                if self.settings.right_border + self.settings.screen_width < self.settings.map_max:
                    self.settings.left_border += min(velocityx + 3, self.settings.map_max - self.settings.right_border)


            # 如果英雄向左移而且到了屏幕左方1/10位置
            if velocityx < 0 and rect.left <= self.settings.screen_width / 10:
                # 如果地图左边界没有到最左边的位置
                if self.settings.left_border > 0:
                    self.settings.left_border -= min(-velocityx, self.settings.left_border)

        # 右边界总是等于左边界加上屏幕宽度
        self.settings.right_border = self.settings.left_border + self.settings.screen_width

    def blitme(self):
        point_list = []
        # pygame.draw.aalines(self.screen, (0, 0, 0), False, point_list, False)
        for i in range(self.settings.screen_width):
            tmp = self.shape[i + self.settings.left_border]
            if i >= 1:
                if self.shape[i + self.settings.left_border - 1] != tmp:
                    point_list.append((i, max(self.shape[i + self.settings.left_border - 1], tmp)))
                    # point_list.append((i, self.shape[i+self.settings.left_border-1]))
            point_list.append((i, tmp))

        pygame.draw.aalines(self.screen, (0, 0, 0), False, point_list, False)

    def gety(self, x):
        if x < 0 or x >= self.settings.map_max:
            return 0
        elif x < self.settings.map_max:
            return self.shape[x]
