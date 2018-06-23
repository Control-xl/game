import math
import pygame

class MonsterBall():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        # 怪物中心位置
        self.center_x = 800
        self.center_y = 400
        # 怪物中心受攻击范围
        self.center_radius = 100
        # 怪物中心移动速度
        self.center_speed = settings.center_speed
        # 怪物血量
        self.blood = settings.blood

        # 怪物保护圈半径
        self.protection_radius = settings.protection_radius

        # 怪物保护圈数目
        self.protection_number = settings.protection_number
        # 怪物保护圈转动速度
        self.protection_speed = settings.protection_speed
        # 怪物保护圈离中心的距离
        self.protection_center_distance = settings.protection_center_distance
        # 保护圈位置确定
        self.protection_position = 0


    def update(self, weapon):
        self.check_collisions(weapon)
        self.protection_position = (self.protection_position + self.protection_speed) % 360
        self.center_x += self.center_speed

    def blitme(self):
        pygame.draw.circle(self.screen, (0, 0, 0), (int(self.center_x), self.center_y), self.center_radius)
        protection_range = int(360 / self.protection_number)
        for i in range(self.protection_number):
            pst_x = int(self.center_x + self.protection_center_distance * \
                    math.cos(math.radians(self.protection_position + i * protection_range)))
            pst_y = int(self.center_y + self.protection_center_distance * \
                    math.sin(math.radians(self.protection_position + i * protection_range)))
            pygame.draw.circle(self.screen, (50, 50, 50), (pst_x, pst_y), self.protection_radius)

    def check_collisions(self, weapon):
        for bullet in weapon.bullets:
            if(self.bullet_collisions(bullet))



    def bullet_collisions(self, bullet):
        if

class MonsterPlane():

    def __init__(self):
        self.a = 1
