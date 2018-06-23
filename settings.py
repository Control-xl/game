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
        # 屏幕背景颜色
        self.bg_color = (252, 252, 252)

        # 地图在屏幕上显示的左边界和右边界
        self.left_border = 0
        self.right_border = 1200

        # 整个地图的最大长度
        self.map_max = 12000

        # 暂停选项
        self.pause = False
        self.pause_bg_color = (157, 157, 157)
        # for test
        self.ship_speed_factor = 2

        # 怪物1号的中心移动速度
        self.center_speed = 0.1
        # 怪物1号的保护圈数量
        self.protection_number = 5
        # 怪物1号保护圈转动速度
        self.protection_speed = 0.1
        # 怪物1号保护圈离中心距离
        self.protection_center_distance = 200



        # 英雄位置,状态
        self.hero_bottom = 800
        self.hero_center = 600
        self.hero_weapon_size = 3
        self.hero_weapon = {
            "fist" : 0,
            "sword" : 1,
            "gun" : 2,
        }
        self.hero_status = {
            "stay" : 0,
            "move" : 1,
            "jump" : 2,
            "fall" : 3,
            "squat" : 4,
            "squat_move" : 5,
            "attack" : 6,
            "jump_attack" : 7,
            "squat_attack" : 8,
            "hurt" : 9,
        }
        self.hero_direction = {"left" : -1, "right" : 1}

        # 英雄初始血量
        self.hero_init_blood = 3
        self.hero_init_magic = 1

