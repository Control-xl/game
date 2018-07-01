import math
import pygame

class MonsterBall():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        # 怪物中心位置
        self.center_x = 1000
        self.center_y = 500
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
        self.protection_blood = [1 for i in range(5)]

        # 是否存活
        self.alive = True

    def update(self, hero):
        if self.blood < 0:
            self.alive = 0
        else:
            self.check_collisions(hero.weapon_attacks)
            self.protection_position = (self.protection_position + self.protection_speed) % 360
            self.center_x -= self.center_speed


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
        if weapon.sword_attacking:
            if self.check_sword_coll(weapon.sword):
                weapon.sword_attacking = False
        if weapon.fist_attacking:
            if self.check_fist_coll(weapon.fist):
                weapon.fist_attacking = False
        if weapon.fist_magic_firing:
            if self.check_fist_magic_coll(weapon):
                weapon.fist_magic_firing = False
        if weapon.sword_magic_firing:
            if self.check_sword_magic_coll(weapon):
                weapon.sword_magic_firing = False

    def check_bullet_coll(self, bullets):
        bullets_to_delete = []
        for bullet in bullets:
            if self.protection_rect_collisions(bullet.rect, self.settings.bullet_damage):
                bullets_to_delete.append(bullet)
            elif self.center_rect_collisions(bullet.rect, self.settings.bullet_damage):
                bullets_to_delete.append(bullet)

        for bullet in bullets_to_delete:
            bullets.remove(bullet)

    def protection_rect_collisions(self, rect, damage):
        """判断矩形和保护圈有没有碰撞"""
        for i in range(self.protection_number):
            if self.protection_blood[i] > 0:
                # 计算保护圈的位置
                pst_x = int(self.center_x + self.protection_center_distance * \
                            math.cos(math.radians(self.protection_position + i * self.protection_range)))
                pst_y = int(self.center_y + self.protection_center_distance * \
                            math.sin(math.radians(self.protection_position + i * self.protection_range)))
                # 矩形左上角计算
                flag = False
                if get_distance2(pst_x, pst_y, rect.left, rect.top) < self.protection_radius**2:
                    flag = True
                # 矩形右上角
                elif get_distance2(pst_x, pst_y, rect.right, rect.top) < self.protection_radius**2:
                    flag = True
                # 矩形左下角
                elif get_distance2(pst_x, pst_y, rect.left, rect.bottom) < self.protection_radius**2:
                    flag = True
                # 矩形右下角
                elif get_distance2(pst_x, pst_y, rect.right, rect.bottom) < self.protection_radius**2:
                    flag = True

                if flag:
                    self.protection_blood[i] -= damage
                    return True
        # 如果没有一个碰撞，返回false
        return False

    # def bullet_protection_collisions(self, bullet):
    #     for i in range(self.protection_number):
    #         if self.protection_blood[i] > 0:
    #             # 计算保护圈的位置
    #             pst_x = int(self.center_x + self.protection_center_distance * \
    #                         math.cos(math.radians(self.protection_position + i * self.protection_range)))
    #             pst_y = int(self.center_y + self.protection_center_distance * \
    #                         math.sin(math.radians(self.protection_position + i * self.protection_range)))
    #             # 子弹左上角计算
    #             flag = False
    #             if get_distance2(pst_x, pst_y, bullet.rect.left, bullet.rect.top) < self.protection_radius**2:
    #                 flag = True
    #             # 子弹右上角
    #             elif get_distance2(pst_x, pst_y, bullet.rect.right, bullet.rect.top) < self.protection_radius**2:
    #                 flag = True
    #             # 子弹左下角
    #             elif get_distance2(pst_x, pst_y, bullet.rect.left, bullet.rect.bottom) < self.protection_radius**2:
    #                 flag = True
    #             # 子弹右下角
    #             elif get_distance2(pst_x, pst_y, bullet.rect.right, bullet.rect.bottom) < self.protection_radius**2:
    #                 flag = True
    #
    #             if flag:
    #                 self.protection_blood[i] -= self.settings.bullet_damage
    #                 return True
    #     # 如果没有一个碰撞，返回false
    #     return False

    def center_rect_collisions(self, rect, damage):
        """判断中心和矩阵有没有碰撞"""
        flag = False
        # 左上
        if get_distance2(self.center_x, self.center_y, rect.left, rect.top) < self.center_radius**2:
            flag = True
        # 右上
        elif get_distance2(self.center_x, self.center_y, rect.right, rect.top) < self.center_radius**2:
            flag = True
        # 左下
        elif get_distance2(self.center_x, self.center_y, rect.left, rect.top) < self.center_radius**2:
            flag = True
        # 右下
        elif get_distance2(self.center_x, self.center_y, rect.left, rect.top) < self.center_radius**2:
            flag = True

        if flag:
            self.blood -= damage

        return flag

    # def bullet_center_collisions(self, bullet):
    #     flag = False
    #     # 左上
    #     if get_distance2(self.center_x, self.center_y, bullet.rect.left, bullet.rect.top) < self.center_radius**2:
    #         flag = True
    #     # 右上
    #     elif get_distance2(self.center_x, self.center_y, bullet.rect.right, bullet.rect.top) < self.center_radius**2:
    #         flag = True
    #     # 左下
    #     elif get_distance2(self.center_x, self.center_y, bullet.rect.left, bullet.rect.top) < self.center_radius**2:
    #         flag = True
    #     # 右下
    #     elif get_distance2(self.center_x, self.center_y, bullet.rect.left, bullet.rect.top) < self.center_radius**2:
    #         flag = True
    #
    #     if flag:
    #         self.blood -= self.settings.bullet_damage
    #
    #     return flag

    def check_sword_coll(self, sword):
        flag1 = self.check_sword_protection_collisions(sword)
        flag2 = self.check_sword_center_collisions(sword)
        return flag1 | flag2

    def check_sword_protection_collisions(self, sword):
        # 检查剑和保护圈是否有碰撞
        for i in range(self.protection_number):
            if self.protection_blood[i] > 0:
                pst_x = int(self.center_x + self.protection_center_distance * \
                            math.cos(math.radians(self.protection_position + i * self.protection_range)))
                pst_y = int(self.center_y + self.protection_center_distance * \
                            math.sin(math.radians(self.protection_position + i * self.protection_range)))

                # 先判断两圆是否相交
                if get_distance2(pst_x, pst_y, sword["centerx"], sword["centery"]) < \
                        (sword["radius"] + self.protection_radius) ** 2:
                    # 判断方向和位置
                    if (sword["centerx"] < pst_x and sword["direction"] == 1) or \
                            (sword["centerx"] > pst_x and sword["direction"] == -1):
                        self.protection_blood[i] -= self.settings.sword_damage
                        return True
        return False

    def check_sword_center_collisions(self, sword):
        # 检测剑和中心的碰撞
        if get_distance2(self.center_x, self.center_y, sword["centerx"], sword["centery"]) < \
                (sword["radius"] + self.center_radius) ** 2:
            if (sword["centerx"] < self.center_x and sword["direction"] == 1) or \
                    (sword["centerx"] > self.center_x and sword["direction"] == -1):
                self.blood -= self.settings.sword_damage
                return True
        return False

    def check_fist_coll(self, fist):
        # 检测拳头的碰撞
        flag1 = self.protection_rect_collisions(fist, self.settings.fist_damage)
        flag2 = self.center_rect_collisions(fist, self.settings.fist_damage)
        return flag1 | flag2

    def check_fist_magic_coll(self, weapon):
        flag1 = self.protection_rect_collisions(weapon.fist_magic, weapon.fist_magic_damage)
        flag2 = self.center_rect_collisions(weapon.fist_magic, weapon.fist_magic_damage)
        return flag1 | flag2

    def check_sword_magic_coll(self, weapon):
        flag1 = self.protection_rect_collisions(weapon.sword_magic, weapon.sword_magic_damage)
        flag2 = self.center_rect_collisions(weapon.sword_magic, weapon.sword_magic_damage)
        return flag1 | flag2

    # def check_fist_protection_collisions(self, fist):
    #     # 检查拳头和保护圈的碰撞
    #     for i in range(self.protection_number):
    #         if self.protection_blood[i] > 0:
    #             pst_x = int(self.center_x + self.protection_center_distance * \
    #                         math.cos(math.radians(self.protection_position + i * self.protection_range)))
    #             pst_y = int(self.center_y + self.protection_center_distance * \
    #                         math.sin(math.radians(self.protection_position + i * self.protection_range)))
    #             if get_distance2(pst_x, pst_y, fist.right, fist.top) < \
    #                 self.protection_radius ** 2 or get_distance2(pst_x, pst_y, fist.right, fist.bottom) < \
    #                 self.protection_radius ** 2:
    #                 self.protection_blood[i] -= self.settings.fist_damage
    #                 return True
    #
    #     return False

    # def check_fist_center_collisions(self, fist):
    #     # 检测拳头和中心的碰撞
    #     if get_distance2(self.center_x, self.center_y, fist.right, fist.top) < self.center_radius ** 2 or \
    #             get_distance2(self.center_x, self.center_y, fist.right, fist.bottom) < self.center_radius ** 2:
    #         self.blood -= self.settings.fist_damage
    #         return True
    #     return False


def get_distance2(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2


class MonsterPlane():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        # 加载飞船
        self.image = pygame.image.load("images/plane.png")
        # 加载飞船蓄力图像
        self.save_energy_image = []
        self.save_energy_image.append(pygame.image.load("images/laser/save1.png"))
        self.save_energy_image.append(pygame.image.load("images/laser/save2.png"))
        self.save_energy_image.append(pygame.image.load("images/laser/save3.png"))
        self.save_energy_image.append(pygame.image.load("images/laser/save4.png"))
        self.save_energy_image.append(pygame.image.load("images/laser/save5.png"))
        # 蓄力形态
        self.save_energy_image_cnt = 0
        # 蓄力图像位置(在飞碟下多少位置
        self.save_energy_image_down = 28
        self.rect = self.image.get_rect()
        self.save_rect = []
        # 蓄力后的子弹列表
        self.bullet_list = []
        self.bullet_rect_list = []
        self.bullet_center_list = []
        self.bullet_dir_list = []
        self.bullet_ud_list = [1, 1, 1, 1, 1, 1]
        # 蓄力状态
        self.save_state = False
        # 开火状态
        self.fire_state = False
        # 子弹速度
        self.bullet_speed = 0.2
        # 子弹位置

        for i in range(5):
            self.save_rect.append(self.save_energy_image[i].get_rect())
        self.clock = pygame.time.Clock()
        self.time_passed = 0
        self.blood = 10
        self.rect.x = 400
        self.rect.y = 400


    def update(self, hero):
        if self.blood > 0:
            # 更新子弹位置
            self.update_bullet()
            # 检测碰撞
            self.check_collisions(hero.weapon_attacks)
            # 计时
            self.time_passed += self.clock.tick()
            # 如果不是在蓄能状态，那么就等待，直到非蓄能状态时间达到5秒
            if not self.save_state:
                if self.time_passed > 5000:
                    self.time_passed = 0
                    self.save_state = True
            else:
                # 如果在蓄能状态，那就0.25秒更新一次状态图，5次更新后发射
                if self.time_passed >= 250:
                    self.save_energy_image_cnt = (self.save_energy_image_cnt + 1) % 6
                    if len(self.bullet_list) < 3:
                        if self.save_energy_image_cnt == 5:
                            print(len(self.bullet_list))
                            self.add_bullet(hero)
                    else:
                        self.save_state = False

                    self.time_passed = 0
                if self.save_energy_image_cnt < 5:
                    self.save_rect[self.save_energy_image_cnt].centerx = self.rect.centerx
                    self.save_rect[self.save_energy_image_cnt].centery = self.rect.bottom + self.save_energy_image_down


    def update_bullet(self):

        if self.bullet_list:
            image_to_del = []
            rect_to_del = []
            center_to_del = []
            dir_to_del = []
            for i in range(len(self.bullet_list)):
                self.bullet_center_list[i] = (self.bullet_center_list[i][0] +
                                              math.sin(self.bullet_dir_list[i]) *
                                              self.bullet_speed * self.bullet_ud_list[i],
                                              self.bullet_center_list[i][1] +
                                              math.cos(self.bullet_dir_list[i]) *
                                              self.bullet_speed * self.bullet_ud_list[i])
                self.bullet_rect_list[i].centerx = self.bullet_center_list[i][0]
                self.bullet_rect_list[i].centery = self.bullet_center_list[i][1]
                # 如果飞出屏幕外，加入删除列表
                if self.bullet_rect_list[i].centerx < -300 or self.bullet_rect_list[i].centerx > 1500 or \
                    self.bullet_rect_list[i].centery < -300 or self.bullet_rect_list[i].centery > 1100:
                    image_to_del.append(self.bullet_list[i])
                    rect_to_del.append(self.bullet_rect_list[i])
                    center_to_del.append(self.bullet_center_list[i])
                    dir_to_del.append(self.bullet_dir_list[i])
            # 删除子弹列表中有的子弹
            for i in range(len(image_to_del)):
                self.bullet_list.remove(image_to_del[i])
                self.bullet_rect_list.remove(rect_to_del[i])
                self.bullet_center_list.remove(center_to_del[i])
                self.bullet_dir_list.remove(dir_to_del[i])
        return

    def add_bullet(self, hero):
        bullet = pygame.image.load('images/laser/bullet.png')
        i = len(self.bullet_list)
        self.bullet_list.append(bullet)
        rect = bullet.get_rect()
        rect.centerx = self.rect.centerx
        rect.centery = self.rect.bottom + self.save_energy_image_down
        self.bullet_rect_list.append(rect)
        self.bullet_center_list.append((self.bullet_rect_list[-1].centerx, self.bullet_rect_list[-1].centery))
        if rect.centery != hero.rect.centery:
            k = (hero.rect.centerx - rect.centerx) / (hero.rect.centery - rect.centery)
        else:
            k = 99999999
        if rect.centery < hero.rect.centery:
            self.bullet_ud_list[i] = 1
        else:
            self.bullet_ud_list[i] = -1
        theta = math.atan(k)
        self.bullet_dir_list.append(theta)

    def check_collisions(self, weapon):
        self.check_bullet_coll(weapon.bullets)
        if weapon.sword_attacking:
            if self.check_sword_coll(weapon.sword):
                weapon.sword_attacking = False
        if weapon.fist_attacking:
            if self.check_rect_coll(weapon.fist, self.settings.fist_damage):
                weapon.fist_attacking = False
        if weapon.fist_magic_firing:
            if self.check_rect_coll(weapon.fist_magic, weapon.fist_magic_damage):
                weapon.fist_magic_firing = False
        if weapon.sword_magic_firing:
            if self.check_rect_coll(weapon.sword_magic, weapon.sword_magic_damage):
                weapon.sword_magic_firing = False

    def check_bullet_coll(self, bullets):
        # 判断子弹是否和飞机发生碰撞
        bullets_to_del = []
        for bullet in bullets:
            # 子弹的矩形碰到飞船的矩形
            # if self.point_coll(bullet.rect.right, bullet.rect.top) or self.point_coll(bullet.rect.right, bullet.rect.bottom):
            #     bullets_to_del.append(bullet)
            if self.check_rect_coll(bullet.rect, self.settings.bullet_damage):
                bullets_to_del.append(bullet)
        for bullet in bullets_to_del:
            bullets.remove(bullet)

    def check_sword_coll(self, sword):
        # 矩形的四个点在圆中或者半圆的三个最远点在矩形中，则视为碰撞
        # 依次判断左上角、左下角、右下角、右上角
        if get_distance2(sword["centerx"], sword["centery"], self.rect.left, self.rect.top) < sword["radius"] ** 2 \
                or \
                get_distance2(sword["centerx"], sword["centery"], self.rect.left, self.rect.bottom) < sword["radius"] ** 2 \
                or \
                get_distance2(sword["centerx"], sword["centery"], self.rect.right, self.rect.bottom) < sword["radius"] ** 2 \
                or \
                get_distance2(sword["centerx"], sword["centery"], self.rect.right, self.rect.top) < sword["radius"] ** 2:
            self.blood -= self.settings.sword_damage
            return True
        # 判断半圆三个点，依次为上，前，下
        if self.point_coll(sword["centerx"], sword["centery"] + sword["radius"]) or \
            self.point_coll(sword["centerx"] + sword["direction"] * sword["radius"], sword["centery"]) or \
            self.point_coll(sword["centerx"], sword["centery"] - sword["radius"]):
            self.blood -= self.settings.sword_damage
            return True
        return False

    def check_rect_coll(self, rect, damage):
        if self.point_coll(rect.right, rect.top) or self.point_coll(rect.right, rect.bottom):
            self.blood -= damage
            return True
        return False

    # def check_fist_coll(self, fist):
    #     if self.point_coll(fist.right, fist.top) or self.point_coll(fist.right, fist.bottom):
    #         self.blood -= self.settings.fist_damage
    #         return True
    #     return False

    def point_coll(self, x, y):
        # 判断点是否在飞船的rect中，有则发生碰撞，返回true
        if x >= self.rect.left and x <= self.rect.right and y <= self.rect.bottom and y >= self.rect.top:
            return True
        return False



    def blitme(self):
        if self.blood > 0:
            self.screen.blit(self.image, self.rect)
            if self.save_energy_image_cnt < 5 and self.save_state:
                self.screen.blit(self.save_energy_image[self.save_energy_image_cnt],
                                 self.save_rect[self.save_energy_image_cnt])
            for i in range(len(self.bullet_list)):
                # print(self.bullet_rect_list[i].centerx, self.bullet_rect_list[i].centery)
                self.screen.blit(self.bullet_list[i], self.bullet_rect_list[i])

        # print(self.save_energy_image[self.save_energy_image_cnt].get_rect())


