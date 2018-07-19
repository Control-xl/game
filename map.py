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
        self.max_index = 0
        self.map_init()

    def update(self, hero, monster_list):
        """根据英雄位置和怪物更新地图信息"""

        velocityx = hero.velocityx
        rect = hero.rect
        if self.cnt < self.max_index:
            if hero.x >= self.monster_point[self.cnt]:
                for monster in self.monster_list[self.cnt]:
                    monster_list.append(monster)
                self.cnt += 1

        #
        # 如果有怪物列表中有怪物要求锁屏
        map_lock_local = False
        for monster in monster_list:
            map_lock_local = map_lock_local | monster.map_lock
        self.settings.map_lock = map_lock_local
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

    def map_app(self, height, long):
        for i in range(long):
            self.shape.append(height)


    def map_mid_app(self):
        self.map_app(600, 600)

    def monster_point_app(self):
        self.monster_point.append(len(self.shape) + self.settings.screen_width / 3)

    def map_init(self):
        screen = self.screen
        settings = self.settings

        # 地图怪物设计

        # 地图1，飞机1，
        # 过渡段
        # self.map_mid_app()
        # # 怪物出现点：过渡点后1/3屏幕
        # self.monster_point_app()
        # # 怪物
        # self.monster_list.append([monster.MonsterPlane(settings, screen, 1, 10000, 500, 1, len(self.shape)+1000, 500)])
        # # 战斗地图
        # self.map_app(700, 1300)
        #
        #
        # # 地图2,球
        # # 过渡段
        # self.map_mid_app()
        # self.monster_point_app()
        # self.monster_list.append([monster.MonsterBall(settings, screen, 0, 5, 5,len(self.shape) + 1000, 400, 0.1, 0.5)])
        # self.map_app(700, 1300)
        #
        # # 3球
        # self.map_mid_app()
        # self.monster_point_app()
        # self.monster_list.append([monster.MonsterBall(settings, screen, 5, 5, 1, len(self.shape)+1000, 350, 0.1, 0.5,
        #                                               protection_radius = 50, )])
        # for i in range(13):
        #     self.map_app(600, 50)
        #     self.map_app(700, 50)
        #
        #
        # # 4飞机 * 2
        # self.map_mid_app()
        # self.monster_point_app()
        # self.monster_list.append([monster.MonsterPlane(settings, screen, 2, 10000, 1000, 10, len(self.shape) + 1000, 520),
        #                           monster.MonsterPlane(settings, screen, 2, 3000, 1000, 1, len(self.shape) + 1000, 200)])
        # self.map_app(700, 1300)
        #
        # # 5球
        # self.map_mid_app()
        # self.monster_point_app()
        # self.monster_list.append([monster.MonsterBall(settings, screen, 3, 7, 3, len(self.shape)+1000, 500, 1, 0.1,
        #                                               protection_radius = 10, center_radius=20)])
        # self.map_app(700, 1300)
        #
        #
        # # 6，障碍躲避关
        # tmp_list = []
        # self.map_mid_app()
        # self.monster_point_app()
        # self.map_mid_app()
        # self.map_app(600, 100)
        #
        # self.map_app(500, 100)
        # self.map_app(self.settings.BOTTOM_NUM, 150)
        # tmp_list.append(monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape)-50, 0, 0, 0, 1.5, 10, 0,
        #                                     False))
        # tmp_list.append(monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape) - 100, 500, 0, 0, 2, 10, 0,
        #                                     False))
        # self.map_app(400, 100)
        # self.map_app(self.settings.BOTTOM_NUM, 200)
        # tmp_list.append(monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape) - 50, 0, 0, 0, 3, 10, 0,
        #                                     False))
        # tmp_list.append(monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape) - 100, 500, 0, 0, 2.5, 10, 0,
        #                                     False))
        # self.map_app(300, 100)
        # for i in range(350):
        #     self.shape.append(700)
        # self.monster_list.append(tmp_list)

        # 飞机，依次为血量，攻击准备时间，蓄力时间，最大子弹数，x，y
        # 球，以此为保护圈血量，中心血量，保护圈数目，初始位置x，y， 保护转速，中心平移速度，y轴移动速度, 中心半径，保护半径
        # 是否锁地图，左边界，右边界

        # # 7 球加障碍物
        # self.map_mid_app()
        # self.monster_point_app()
        # self.map_app(600, 400)
        # self.monster_list.append([monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape) + 900, 450, 0, 5, 0,
        #                                               20, 1, False, len(self.shape)+100, len(self.shape)+1300),
        #                           monster.MonsterPlane(settings, screen, 7, 5000, 3000, 2, len(self.shape) + 900, 400, False)])
        # for i in range(7):
        #     self.map_app(600, 100)
        #     self.map_app(700, 100)


        # map 8
        self.map_mid_app()
        self.monster_point_app()
        self.map_mid_app()
        self.monster_list.append([monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape) + 800, 400, 0, 0,
                                     5, 20, 1, False),
                                  monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape) + 550, 400, 0, 0,
                                     5, 20, 1, False),
                                  monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape) + 300, 400, 0, 0,
                                                      5, 20, 1, False),
                                  monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape) , 585, 0, 3,
                                                      0, 20, 1, False, len(self.shape)+100, len(self.shape)+1300),
                                  monster.MonsterBall(settings, screen, 0, 999999, 1, len(self.shape), 585, 0, 3,
                                                      3, 20, 1, False, len(self.shape) + 100, len(self.shape) + 1300)
                                  ])
        for i in range(5):
            self.map_app(settings.BOTTOM_NUM, 100)
            self.map_app(600, 150)

        # self.monster_list.append([monster.MonsterBall(settings, screen, 1, 10, 5, 1100, 500, 0.1, 0.1)])


        # for test
        # 怪物组数
        self.max_index = len(self.monster_list)

        # to del
        self.monster_point.append(600)
        self.monster_point.append(2300)

        for i in range(1200):
            self.shape.append(400)