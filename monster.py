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
        # 保护圈和保护圈之间的间隔
        self.protection_range = int(360 / self.protection_number)
        # 保护圈位置确定
        self.protection_position = 0
        # 保护圈颜色
        self.protection_color = settings.monster_ball_protection_color
        self.protection_blood = [20, 20, 20, 20, 20]

        # 是否存活
        self.alive = True

    def update(self, weapon):
        if self.blood < 0:
            self.alive = 0
        else:
            self.check_collisions(weapon)
            self.protection_position = (self.protection_position + self.protection_speed) % 360
            self.center_x += self.center_speed


    def blitme(self):
        if not self.alive:
            return

        if self.blood > 0:
            pygame.draw.circle(self.screen, (0, 0, 0), (int(self.center_x), self.center_y), self.center_radius)

        for i in range(self.protection_number):
            if self.protection_blood[i] != 0:
                pst_x = int(self.center_x + self.protection_center_distance * \
                        math.cos(math.radians(self.protection_position + i * self.protection_range)))
                pst_y = int(self.center_y + self.protection_center_distance * \
                        math.sin(math.radians(self.protection_position + i * self.protection_range)))
                pygame.draw.circle(self.screen, self.protection_color[i], (pst_x, pst_y), self.protection_radius)

    def check_collisions(self, weapon):
        self.check_bullet_coll(weapon.bullets)
        # TODO:需要一个剑和出拳的状态标志
        self.check_sword_coll(weapon.sword)

        self.check_fist_coll(weapon.fist)

    def check_bullet_coll(self, bullets):
        # print(len(bullets))
        bullets_to_delete = []
        for bullet in bullets:
            if self.bullet_protection_collisions(bullet):
                print("ok, in protect remove", bullet)
                bullets_to_delete.append(bullet)
            elif self.bullet_center_collisions(bullet):
                print("ok, in heart1", bullet)
                bullets_to_delete.append(bullet)

        for bullet in bullets_to_delete:
            bullets.remove(bullet)

    def bullet_protection_collisions(self, bullet):
        for i in range(self.protection_number):
            if self.protection_blood[i] > 0:
                # 计算保护圈的位置
                pst_x = int(self.center_x + self.protection_center_distance * \
                            math.cos(math.radians(self.protection_position + i * self.protection_range)))
                pst_y = int(self.center_y + self.protection_center_distance * \
                            math.sin(math.radians(self.protection_position + i * self.protection_range)))
                # 子弹左上角计算
                flag = False
                if get_distance2(pst_x, pst_y, bullet.rect.left, bullet.rect.top) < self.protection_radius**2:
                    flag = True
                # 子弹右上角
                elif get_distance2(pst_x, pst_y, bullet.rect.right, bullet.rect.top) < self.protection_radius**2:
                    flag = True
                # 子弹左下角
                elif get_distance2(pst_x, pst_y, bullet.rect.left, bullet.rect.bottom) < self.protection_radius**2:
                    flag = True
                # 子弹右下角
                elif get_distance2(pst_x, pst_y, bullet.rect.right, bullet.rect.bottom) < self.protection_radius**2:
                    flag = True

                if flag:
                    self.protection_blood[i] -= self.settings.bullet_damage
                    return True
        # 如果没有一个碰撞，返回false
        return False

    def bullet_center_collisions(self, bullet):
        flag = False
        # 左上
        if get_distance2(self.center_x, self.center_y, bullet.rect.left, bullet.rect.top) < self.center_radius**2:
            flag = True
        # 右上
        elif get_distance2(self.center_x, self.center_y, bullet.rect.right, bullet.rect.top) < self.center_radius**2:
            flag = True
        # 左下
        elif get_distance2(self.center_x, self.center_y, bullet.rect.left, bullet.rect.top) < self.center_radius**2:
            flag = True
        # 右下
        elif get_distance2(self.center_x, self.center_y, bullet.rect.left, bullet.rect.top) < self.center_radius**2:
            flag = True

        if flag:
            self.blood -= self.settings.bullet_damage

        return flag

    def check_sword_coll(self, sword):
        self.check_sword_protection_collisions(sword)
        self.check_sword_center_collisions(sword)

    def check_sword_protection_collisions(self, sword):
        for i in range(self.protection_number):
            if self.protection_blood[i] > 0:
                pst_x = int(self.center_x + self.protection_center_distance * \
                            math.cos(math.radians(self.protection_position + i * self.protection_range)))
                pst_y = int(self.center_y + self.protection_center_distance * \
                            math.sin(math.radians(self.protection_position + i * self.protection_range)))
                if get_distance2(pst_x, pst_y, sword["centerx"], sword["centery"]) < \
                        (sword["radius"] + self.protection_radius) ** 2:
                    self.protection_blood[i] -= self.settings.blood_damage

    def check_sword_center_collisions(self, sword):
        if get_distance2(self.center_x, self.center_y, sword["centerx"], sword["centery"]) < \
                (sword["radius"] + self.center_radius) ** 2:
            self.blood -= self.settings.blood_damage

    def check_fist_coll(self, fist):
        return 1


def get_distance2(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2


class MonsterPlane():

    def __init__(self):
        self.a = 1
