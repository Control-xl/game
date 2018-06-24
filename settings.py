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
        self.bg_color = (255, 255, 255)

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
        self.center_speed = 0.03
        # 怪物1号血量
        self.blood = 5
        # 怪物1号的保护圈数量
        self.protection_number = 5
        # 怪物1号保护圈半径
        self.protection_radius = 75
        # 怪物1号保护圈转动速度
        self.protection_speed = 0.1
        # 怪物1号保护圈离中心距离
        self.protection_center_distance = 200
        # 怪物1号保护圈颜色
        self.monster_ball_protection_color = [(0xFA, 0x00, 0x00), (0x00, 0x00, 0xC6),
                                 (0xFF, 0xFF, 0x37), (0x00, 0xBB, 0x00),
                                 (0xAE, 0x57, 0xA4)]

        self.sword_damage = 2
        self.bullet_damage = 1
        self.fist_damage = 1


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
            "attack" : 3,
            "jump_attack" : 4,
            "hurt" : 5,
            "fall" : 6,
            "squat" : 7,
            "squat_move" : 8,
            "squat_attack" : 9,
            
        }
        self.hero_direction = {"left" : -1, "right" : 1}

        # 英雄初始血量
        self.hero_init_blood = 3
        self.hero_init_magic = 1

