import math
import pygame

class MonsterBall():
    def __init__(self, settings, screen, protection_blood = 1, center_blood = 1, protection_num = 1, x = 1000, y = 500,
                 protection_speed = 0.1, center_speed = 0.03):
        self.settings = settings
        self.screen = screen
        # 怪物中心位置
        self.center_x = x
        self.center_y = y
        # 怪物中心受攻击范围
        self.center_radius = 100
        # 怪物中心移动速度
        self.center_speed = center_speed
        # 怪物血量
        self.blood = center_blood

        # 怪物保护圈半径
        self.protection_radius = settings.protection_radius

        # 怪物保护圈数目
        self.protection_number = protection_num
        # 怪物保护圈转动速度
        self.protection_speed = protection_speed
        # 怪物保护圈离中心的距离
        self.protection_center_distance = settings.protection_center_distance
        # 保护圈和保护圈之间的间隔
        self.protection_range = 0
        if self.protection_number > 0:
            self.protection_range = int(360 / self.protection_number)
        else:
            self.protection_range = 10000
        # 保护圈位置确定
        self.protection_position = 0
        # 保护圈颜色
        self.protection_color = settings.monster_ball_protection_color
        self.protection_blood = [protection_blood for i in range(5)]

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
            if self.protection_blood[i] > 0:
                pst_x = int(self.center_x + self.protection_center_distance *
                            math.cos(math.radians(self.protection_position + i * self.protection_range)))
                pst_y = int(self.center_y + self.protection_center_distance *
                            math.sin(math.radians(self.protection_position + i * self.protection_range)))
                pygame.draw.circle(self.screen, self.protection_color[i], (pst_x, pst_y), self.protection_radius)

    def check_collisions(self, weapon):
        self.check_bullet_coll(weapon.bullets)
        if weapon.sword_attacking:
            if self.check_sword_coll(weapon.sword):
                weapon.sword_attacking = False
        if weapon.fist_attacking:
            print("fist", weapon.fist)
            print("center blood", self.blood)

            if self.check_fist_coll(weapon.fist):
                weapon.fist_attacking = False
        if weapon.fist_magic_firing:
            print("fist magic", weapon.fist_magic)
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

        if bullets_to_delete:
            print("delete bullets", bullets_to_delete)
        for bullet in bullets_to_delete:
            print("rect:", bullet.rect)
            bullets.remove(bullet)



    def protection_rect_collisions(self, rect, damage):
        """判断矩形和保护圈有没有碰撞"""
        for i in range(self.protection_number):
            if self.protection_blood[i] > 0:
                # 计算保护圈的位置
                pst_x = int(self.center_x + self.protection_center_distance *
                            math.cos(math.radians(self.protection_position + i * self.protection_range)))
                pst_y = int(self.center_y + self.protection_center_distance *
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
                # 判断圆的最右端到最左端的点是否在矩形中
                else:
                    init_x = pst_x - self.protection_radius
                    while init_x < pst_x + self.protection_radius:
                        if point_in_rect(init_x, pst_y, rect):
                            flag = True
                            break
                        init_x += rect.width
                if flag:
                    self.protection_blood[i] -= damage
                    return True
        # 如果没有一个碰撞，返回false
        return False

    def center_rect_collisions(self, rect, damage):
        """判断中心和矩阵有没有碰撞"""
        # 先判断矩形的四个角是不是有在圆中
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
        # 再判断圆两端是否在矩形中
            # 判断圆的最右端到最左端的点是否在矩形中
        else:
            init_x = self.center_x - self.protection_radius
            while init_x < self.center_x + self.protection_radius:
                if point_in_rect(init_x, self.center_y, rect):
                    flag = True
                    break
                init_x += rect.width
        if flag:
            self.blood -= damage

        return flag

    def check_sword_coll(self, sword):
        flag1 = self.check_sword_protection_collisions(sword)
        flag2 = self.check_sword_center_collisions(sword)
        return flag1 | flag2

    def check_sword_protection_collisions(self, sword):
        # 检查剑和保护圈是否有碰撞
        for i in range(self.protection_number):
            if self.protection_blood[i] > 0:
                pst_x = int(self.center_x + self.protection_center_distance *
                            math.cos(math.radians(self.protection_position + i * self.protection_range)))
                pst_y = int(self.center_y + self.protection_center_distance *
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


def get_distance2(x1, y1, x2, y2):
    return (x1 - x2)**2 + (y1 - y2)**2


class MonsterPlane():
    def __init__(self, settings, screen, blood=1, save_time=5000, fire_time=250, x=1000, y=500):
        self.settings = settings
        self.screen = screen
        # 加载飞船
        self.image = pygame.image.load("images/plane.png")
        # 飞船位置
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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

        self.save_rect = []
        # 蓄力后的子弹列表
        self.bullet_list = []
        self.bullet_rect_list = []
        self.bullet_center_list = []
        self.bullet_dir_list = []
        self.bullet_ud_list = []
        self.bullet_alive_list = []
        # 蓄力状态
        self.save_state = False
        # 蓄力时间/ms
        self.save_time = save_time
        # 开火时间/ms
        self.fire_time = fire_time
        # 开火状态
        self.fire_state = False
        # 子弹上限
        self.max_bullet_num = 3
        # 子弹速度
        self.bullet_speed = 0.5
        # 子弹位置
        for i in range(5):
            self.save_rect.append(self.save_energy_image[i].get_rect())
        self.clock = pygame.time.Clock()
        self.time_passed = 0
        self.blood = blood

        # 子弹一共存在3发后的停火标志（停止计时）
        self.full_energy = False

    def update(self, hero):
        if self.blood > 0:
            # 更新子弹位置
            self.update_bullet()
            # 检测碰撞
            self.check_collisions(hero.weapon_attacks)
            # 计算子弹数
            cnt = 0
            for i in range(len(self.bullet_list)):
                if self.bullet_alive_list[i]:
                    cnt += 1
            # 计时
            self.time_passed += self.clock.tick()
            if self.full_energy and cnt > 0:
                self.time_passed = 0
                return
            else:
                self.full_energy = False
            # 如果不是在蓄能状态，那么就等待，直到非蓄能状态时间达到save_time毫秒，默认5秒一次
            if not self.save_state:
                if self.time_passed > self.save_time:
                    self.time_passed = 0
                    self.save_state = True
            else:
                # 如果在蓄能状态，那就fire_time毫秒（默认0.25秒）更新一次状态图，5次更新后发射
                if self.time_passed >= self.fire_time:
                    self.save_energy_image_cnt = (self.save_energy_image_cnt + 1) % 6
                    if cnt < self.max_bullet_num:
                        if self.save_energy_image_cnt == 5:
                            self.add_bullet(hero)
                    else:
                        self.save_state = False
                        self.full_energy = True

                    self.time_passed = 0
                if self.save_energy_image_cnt < 5:
                    self.save_rect[self.save_energy_image_cnt].centerx = self.rect.centerx
                    self.save_rect[self.save_energy_image_cnt].centery = self.rect.bottom + self.save_energy_image_down

    def update_bullet(self):
        max_ = min(len(self.bullet_list), self.max_bullet_num)
        for i in range(max_):
            if self.bullet_alive_list[i]:
                self.bullet_center_list[i] = (self.bullet_center_list[i][0] +
                                              math.sin(self.bullet_dir_list[i]) *
                                              self.bullet_speed * self.bullet_ud_list[i],
                                              self.bullet_center_list[i][1] +
                                              math.cos(self.bullet_dir_list[i]) *
                                              self.bullet_speed * self.bullet_ud_list[i])
                self.bullet_rect_list[i].centerx = self.bullet_center_list[i][0]
                self.bullet_rect_list[i].centery = self.bullet_center_list[i][1]
                # 如果飞出屏幕外，状态改为False
                if self.bullet_rect_list[i].centerx < -300 or self.bullet_rect_list[i].centerx > 1500 or \
                        self.bullet_rect_list[i].centery < -300 or self.bullet_rect_list[i].centery > 1100:
                    self.bullet_alive_list[i] = False
        return

    def add_bullet(self, hero):
        if len(self.bullet_list) < self.max_bullet_num:
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
                self.bullet_ud_list.append(1)
            else:
                self.bullet_ud_list.append(-1)
            theta = math.atan(k)
            self.bullet_dir_list.append(theta)
            self.bullet_alive_list.append(True)
            return
        fst_disable_bullet = self.max_bullet_num
        for i in range(self.max_bullet_num):
            if not self.bullet_alive_list[i]:
                fst_disable_bullet = i
                break
            i += 1
        if fst_disable_bullet < self.max_bullet_num:
            bullet = self.bullet_list[fst_disable_bullet]
            rect = bullet.get_rect()
            rect.centerx = self.rect.centerx
            rect.centery = self.rect.bottom + self.save_energy_image_down
            self.bullet_rect_list[fst_disable_bullet] = rect
            self.bullet_center_list[fst_disable_bullet] = (self.bullet_rect_list[fst_disable_bullet].centerx,
                                                           self.bullet_rect_list[fst_disable_bullet].centery)
            if rect.centery != hero.rect.centery:
                k = (hero.rect.centerx - rect.centerx) / (hero.rect.centery - rect.centery)
            else:
                k = 99999999
            if rect.centery < hero.rect.centery:
                self.bullet_ud_list[fst_disable_bullet] = 1
            else:
                self.bullet_ud_list[fst_disable_bullet] = -1
            theta = math.atan(k)
            self.bullet_dir_list[fst_disable_bullet] = theta
            self.bullet_alive_list[fst_disable_bullet] = True
            return

    def check_collisions(self, weapon):
        """检测和角色各种东西的碰撞"""
        self.check_bullet_coll(weapon.bullets)
        if weapon.sword_attacking:
            if self.check_sword_coll(weapon.sword):
                weapon.sword_attacking = False
        if weapon.fist_attacking:
            if self.check_rect_coll(weapon.fist, self.settings.fist_damage):
                weapon.fist_attacking = False
        if weapon.fist_magic_firing:
            print("magic:", weapon.fist_magic, "self at", self.rect)
            if self.check_rect_coll(weapon.fist_magic, weapon.fist_magic_damage):
                print("fist magic success!")
                weapon.fist_magic_firing = False
        if weapon.sword_magic_firing:
            if self.check_rect_coll(weapon.sword_magic, weapon.sword_magic_damage):
                weapon.sword_magic_firing = False

    def check_bullet_coll(self, bullets):
        # 判断子弹是否和飞机发生碰撞
        bullets_to_del = []
        for bullet in bullets:
            # 子弹的矩形碰到飞船的矩形
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
        if self.point_coll(rect.right, rect.top) or self.point_coll(rect.right, rect.bottom) or \
                self.point_coll(rect.left, rect.bottom) or self.point_coll(rect.left, rect.top):
            self.blood -= damage
            return True
        if self.point_coll(self.rect.right, self.rect.top, rect) or \
                self.point_coll(self.rect.right, self.rect.bottom, rect) or \
            self.point_coll(self.rect.left, self.rect.bottom, rect) or \
                self.point_coll(self.rect.left, self.rect.top, rect):
            self.blood -= damage
            return True
        return False

    def point_coll(self, x, y, rect = None):
        # 判断点是否在飞船的rect中，有则发生碰撞，返回true
        if rect == None:
            rect = self.rect
        if rect.left <= x <= rect.right and rect.top <= y <= rect.bottom:
            return True
        return False

    def blitme(self):
        if self.blood > 0:
            self.screen.blit(self.image, self.rect)
            if self.save_energy_image_cnt < 5 and self.save_state:
                self.screen.blit(self.save_energy_image[self.save_energy_image_cnt],
                                 self.save_rect[self.save_energy_image_cnt])
            for i in range(len(self.bullet_list)):
                if self.bullet_alive_list[i]:
                    self.screen.blit(self.bullet_list[i], self.bullet_rect_list[i])


def point_in_rect(x, y, rect):
    if rect.left < x < rect.right and rect.top < y < rect.bottom:
        return True
    return False
