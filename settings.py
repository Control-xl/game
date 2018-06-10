import pygame


class Settings():
    def __init__(self):

        # 音量大小
        self.volume = 0.1
        # 屏幕初始长宽
        # self.init_screen_width = 1200
        # self.init_screen_height = 800
        # 英雄初始位置
        # self.init_hero_bottom = 800
        # self.init_hero_center = 600
        # 屏幕位置
        self.screen_width = 1200
        self.screen_height = 800
        # 英雄位置
        self.hero_bottom = 800
        self.hero_center = 600
        # 屏幕背景颜色
        self.bg_color = (230, 230, 230)



        # 地图在屏幕上显示的左边界和右边界
        self.left_border = 0
        self.right_border = 1200

        # 整个地图的最大长度
        self.map_max = 12000


        # for test

        self.ship_speed_factor = 1


