import pygame
import sys
import math
from settings import Settings
from weapon import Weapon, Bullet
from map import Map
from monster import MonsterBall, MonsterPlane
from game_functions import transparent

class Frame():
    # 代表一个火柴人的外部框架，用以碰撞检测
    # 在火柴人的外表加一层白色的颜色层，当这一层东西颜色变了，发生了碰撞
    # get_at(pos)， set_at(pos, color)表示读取与设置surface中一个像素点的颜色
    def __init__(self, image, settings):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.frame = [] #表示第几行的人物外框
        self.top = self.rect.bottom
        self.bottom = self.rect.top
        self.left = self.rect.right
        self.right = self.rect.left
        for y in range(self.rect.top, self.rect.bottom):
            left = 0
            right = 0
            x = self.rect.left
            while x < self.rect.right :
                (r, g, b, alpha) = image.get_at((x, y))
                if r < 20 and r == g and r == b:
                    left = x
                    break 
                x += 1
            x = self.rect.right
            while x > self.rect.left:
                x -= 1
                (r, g, b, alpha) = image.get_at((x, y))
                if r < 20 and r == g and r == b:
                    right = x
                    break
            if left > right:
                left = 0
                right = 0
            if left > 0 :
                left -= 1
            if right != 0 and right + 1 < self.rect.right :
                right += 1
            self.frame.append({"left" : [], "right" : []})             #
            if left != right:
                self.top = min (y, self.top)
                self.bottom = max(y, self.bottom)
                self.left = min(self.left+1, left)
                self.right = max(self.right-1, right)
                image.set_at((left, y), settings.hero_boot_color)
                image.set_at((right, y), settings.hero_boot_color)
                self.frame[-1]["left"].append(left)
                self.frame[-1]["right"].append(right)
                if len(self.frame) > 1 and len(self.frame[-2]["left"]) > 0 :
                    last = self.frame[-2]["left"][0]
                    this = self.frame[-1]["left"][0]
                    while this != last :
                        #当上下行的外框点不连通时, 连一条线
                        if last > this :
                            last -= 1
                            self.frame[-2]["left"].append(last)
                            image.set_at((last, y-1), settings.hero_boot_color)
                        else :
                            this -= 1
                            self.frame[-1]["left"].append(this)
                            image.set_at((this, y), settings.hero_boot_color)
                if len(self.frame) > 1 and len(self.frame[-2]["right"]) > 0 :
                    last = self.frame[-2]["right"][0]
                    this = self.frame[-1]["right"][0]
                    while this != last :
                        #当上下行的外框点不连通时, 连一条线
                        if last < this :
                            last += 1
                            self.frame[-2]["right"].append(last)
                            image.set_at((last, y-1), settings.hero_boot_color)
                        else :
                            this += 1
                            self.frame[-1]["right"].append(this)
                            image.set_at((this, y), settings.hero_boot_color)


class Hero():
    def __init__(self, screen, map_, settings):
        self.screen = screen
        self.map = map_
        self.settings = settings
        self.frame_order = 0                                                    #正播放的帧序号
        self.frame_size = 5                                                     #代表一个图片要放的帧数目
        self.basic_frame_size = 5                                               #基本帧数目
        self.jump_frame_size = [2,2,2,2,5,5,2,2,8,8,8,8,8,5,5,5,5,]             #用于调节跳跃动作的帧数目
        #                      [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,]
        self.image_order = 0     #正播放的图片序号
        self.move_size = [6, 12, 6]       #移动图片的总数目 6,12,6
        self.attack_size = [11, 8, 0]    # 11, 11, 11
        self.jump_size = 17      # 17, 17, 17
        self.jump_attack_size = [17, 17, 0]   #17, 17, 17
        self.fire_magic_size = [8, 8, 0]
        self.hurt_size = 4       # 4, 4, 4
        self.squat_move_size = 10
        self.squat_attack_size = 9
        self.weapon_size = self.settings.hero_weapon_size
        #images[direction][weapon]代表一个图片或图片文件夹或空
        self.enemy_bullet_image = pygame.image.load('images/laser/bg_bullet.png')
        self.stay_images = {}
        self.move_images = {}
        self.attack_images = {}
        self.jump_images = {}
        self.jump_attack_images = {}
        self.fire_magic_images = {}
        self.hurt_images = {}
        # self.squat_images = {}
        # self.squat_attack_images = {}
        # self.squat_move_images = {}
        self.image_to_frame = {}
        self.load_images()
        self.weapon = self.settings.hero_weapon["fist"]
        self.status = settings.hero_status["stay"]
        self.direction = settings.hero_direction["right"]
        self.image = self.stay_images[self.direction][self.weapon]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
        self.x = self.settings.left_border + self.rect.centerx          #在整个地图中的位置
        self.rect.bottom = self.map.gety(self.rect.centerx)
        self.moving_left = False
        self.moving_right = False
        self.getting_hurt = False
        self.attacking = False
        self.fire_magicing = False
        self.jumping = False
        self.squating = False
        self.falling = False
        self.blood = self.settings.hero_init_blood
        self.magic = self.settings.hero_init_magic
        self.weapon_attacks = Weapon(self.screen, self.settings)
        self.weapon_en = {
            self.settings.hero_weapon["fist"] : True,
            self.settings.hero_weapon["sword"] : True,
            self.settings.hero_weapon["gun"] : True,
        }
        self.jump_en = 1                                #1代表可以
        self.shoot_en = 0                               #shoot_en = 0时才能射击
        self.magic_cd = 0                               #magic_cd = 0时才能进行魔法攻击
        self.hurt_en = 5                                #代表可以攻击，非0时代表无敌
        self.speedy = 8
        self.velocityx = 0
        self.velocityy = -self.speedy
        self.speedx = 4

    def update_status(self):
        #根据旧状态即status的值继续状态;或者根据按键(即or后面)更改状态.更新image
        #可以改变方向的只有 移动键和受伤
        self.frame_size = self.basic_frame_size
        if self.status == self.settings.hero_status["hurt"]:
            #受伤的优先级最高, 要更新图形
            self.hurt_image()
        elif self.status == self.settings.hero_status["fire_magic"]:
            self.fire_magic_image()
        elif self.status == self.settings.hero_status["attack"] :
            #攻击动画
            self.attack_image()
        elif self.status == self.settings.hero_status["jump_attack"] :
            #跳起攻击动画
            self.jump_attack_image()
        elif self.status == self.settings.hero_status["squat_attack"] :
            #下蹲攻击动画
            self.squat_attack_image()
        elif self.fire_magicing == True and self.magic_cd == 0 \
        and self.weapon != self.settings.hero_weapon["gun"]:
            self.image_order = 0
            self.frame_order = 0
            self.status = self.settings.hero_status["fire_magic"]
        elif self.attacking and self.weapon != self.settings.hero_weapon["gun"]:
            #当按下攻击键时，进入攻击状态
            if self.status == self.settings.hero_status["jump"] :
                self.status = self.settings.hero_status["jump_attack"]
            elif self.status == self.settings.hero_status["squat"]:
                self.frame_order = 0
                self.image_order = 0
                self.status = self.settings.hero_status["squat_attack"]
            else :
                self.frame_order = 0
                self.image_order = 0
                self.status = self.settings.hero_status["attack"]
        elif self.status == self.settings.hero_status["jump"] :
            # 跳起
            self.jump_image()
        # elif self.status == self.settings.hero_status["squat_move"]:
        #     #蹲着移动
        #     self.squat_move()
        # elif self.squating :
        #     #下蹲键, 按着蹲下键时，无法跳跃，即按跳起键无效。当此时有移动按键时，将变成蹲着移动
        #     self.status = self.settings.hero_status["squat"]
        #     self.squat_image()
        elif self.jumping :
            #跳跃键
            self.image_order = 0
            self.status = self.settings.hero_status["jump"]
        elif self.status == self.settings.hero_status["move"] :
            # 最后是移动
            self.move_image()
        elif self.moving_left != self.moving_right :
            # 进入移动状态
            self.status = self.settings.hero_status["move"]
            if self.moving_left == True:
                self.direction = self.settings.hero_direction["left"]
            elif self.moving_right == True:
                self.direction = self.settings.hero_direction["right"]
        else : #self.status == self.settings.hero_status["stay"]
            # 静止状态
            self.status = self.settings.hero_status["stay"]
            self.image_order = 0
            self.frame_order = 0
            self.velocityx = 0
            self.velocityy = self.speedy
            self.stay_image()
        #重置
        if self.status != self.settings.hero_status["hurt"]:
            if self.weapon == self.settings.hero_weapon["gun"] and self.attacking: #gun无攻击状态
                self.attacking = False
                self.shoot_bullet()
        if self.shoot_en > 0:
            self.shoot_en -= 1
        if self.hurt_en > 0:
            self.hurt_en -= 1
        if self.magic_cd > 0:
            self.magic_cd -= 1
        self.jumping = False
        self.attacking = False
        self.fire_magicing = False
        

    def get_hurt(self, direction):
        # 发生碰撞时，调用的接口函数，
        # 更新人物方向，设置人物状态,direction表示来自左边的攻击
        # 若人物已经受伤，不再受伤
        if self.status != self.settings.hero_status["hurt"] and self.hurt_en == 0:
            self.direction = direction
            self.status = self.settings.hero_status["hurt"]
            self.image_order = 0
            self.frame_order = 0
            self.hurt_en = 200
#播放动画
    def hurt_image(self):
        #受伤动画，播完动画则结束受伤状态
        self.velocityx = - self.direction * self.speedx
        self.velocityy = self.speedy
        self.change_image(self.hurt_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.hurt_size)

    def attack_image(self):
        #攻击动画
        self.velocityx = 0
        self.velocityy = self.speedy
        self.change_image(self.attack_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.attack_size[self.weapon])

    def jump_attack_image(self):
        #跳起时进行攻击
        # 调节帧数目
        self.frame_size = self.jump_frame_size[self.image_order]
        if self.moving_left == True and self.moving_right == False:
            self.velocityx = -self.speedx
        elif self.moving_left == False and self.moving_right == True:
            self.velocityx = self.speedx
        if self.image_order >= 6 and self.image_order <= 7:
            self.velocityy = -self.speedy
        elif self.image_order >= 8 and self.image_order <= 10:
            self.velocityy = -self.speedy
        elif self.image_order == 11:
            self.velocityy = 0
        else :
            self.velocityy = self.speedy
        self.change_image(self.jump_attack_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.jump_attack_size[self.weapon])

    def jump_image(self):
        #跳跃动画
        #self.velocityx 随移动键改变
        self.frame_size = self.jump_frame_size[self.image_order]
        if self.moving_left == True and self.moving_right == False:
            self.direction = self.settings.hero_direction["left"]
            self.velocityx = -self.speedx
        elif self.moving_left == False and self.moving_right == True:
            self.direction = self.settings.hero_direction["right"]
            self.velocityx = self.speedx
        # 调节帧数目
        if self.image_order >= 6 and self.image_order <= 7:
            self.velocityy = -self.speedy
        elif self.image_order >= 8 and self.image_order <= 10:
            self.velocityy = -self.speedy
        elif self.image_order == 11:
            self.velocityy = 0
        else :
            self.velocityy = self.speedy
        self.change_image(self.jump_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.jump_size)

    def fire_magic_image(self):
        self.velocityx = 0
        self.velocityy = self.speedy
        self.change_image(self.fire_magic_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.fire_magic_size[self.weapon])

    def move_image(self):
        #移动动画, 如果是状态发生改变
        if self.direction == self.settings.hero_direction["left"] and \
        self.moving_left == True and self.moving_right == False :
            self.velocityx = self.speedx * self.direction
        elif self.direction == self.settings.hero_direction["right"] and \
        self.moving_right == True and self.moving_left == False :
            self.velocityx = self.speedx * self.direction
        else :
            self.velocityx = 0
        self.velocityy = self.speedy
        #动画未播放完整，继续动画
        self.change_image(self.move_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.move_size[self.weapon])

    def stay_image(self):
        self.change_image(self.stay_images[self.direction][self.weapon])

    # def squat_image(self):
    #     #下蹲动画,有方向时变成滚动了
    #     if self.moving_left != self.moving_right :
    #         self.status = self.settings.hero_status["squat_move"]
    #         if self.moving_left == True:
    #             self.direction = self.settings.hero_direction["left"]
    #         elif self.moving_right == True:
    #             self.direction = self.settings.hero_direction["right"]
    #     self.change_image(self.squat_right_image)
    # def squat_move(self):
    #     self.velocityx = 2 * self.speedx * self.direction
    #     self.velocityy = -self.speedy
    #     self.change_image(self.squat_move_images[self.direction][self.weapon][self.image_order])
    #     self.display_frame(self.squat_move_size)
    # def squat_attack_image(self):
    #     self.change_image(self.squat_attack_images[self.direction][self.weapon][self.image_order])
    #     self.display_frame(self.squat_attack_size)


    def update_pos(self):
        self.update_herox()
        self.update_heroy()

    def update_herox(self):
        x = self.settings.left_border + self.velocityx + self.rect.centerx
        if self.map.gety(x + self.velocityx * 2) < self.rect.bottom :
            self.velocityx = 0
        if (self.x > self.settings.left_border and self.x < self.settings.left_border + self.settings.screen_width) \
        or (self.x <= self.settings.left_border and self.velocityx > 0)\
        or (self.velocityx < 0 and self.x >= self.settings.left_border + self.settings.screen_width):
            self.x += self.velocityx
            if self.settings.map_lock or \
            (self.velocityx > 0 and self.rect.right < self.settings.screen_width/2) or \
            (self.velocityx < 0 and self.rect.left > self.settings.screen_width/10):
                self.rect.centerx += self.velocityx
        # self.map.update(self.velocityx, self.rect)
        
        

    def update_heroy(self):
        #跳起与坠落
        self.rect.bottom += self.velocityy
        if self.rect.bottom > self.map.gety(self.x):
            self.rect.bottom = self.map.gety(self.x)


    def check_collision(self, monster_list, tool_list):
        #碰撞检测, 碰撞到地图, 道具, 拳头攻击到敌人, 敌人攻击
        #遇到不同颜色，先检查道具，看对应的位置的颜色是否一样，一样则是接触到了道具
        #再检测是不是正在进行拳头攻击，是的话，某些位置不会成为攻击矩形
        #否则受到攻击
        frame = self.image_to_frame[self.image]
        for y in range(frame.top, frame.bottom):
            for direction, xs in frame.frame[y].items() :
                for x in xs :
                    pos = (self.rect.left + x, self.rect.top + y)
                    if pos[0] < 0 or pos[0] >= self.settings.screen_width or \
                    pos[1] < 0 or pos[1] >= self.settings.screen_height :
                        continue
                    color = self.screen.get_at(pos)
                    if color != self.settings.hero_boot_color:
                        #先检测碰撞到什么
                        touch_object = self.touch_object(pos, color, monster_list, tool_list)
                        i = 0
                        if touch_object == "tool" : #道具名称
                            pass
                        elif touch_object == "bullet" :
                            self.get_hurt(self.settings.hero_direction[direction])
                        elif touch_object == "enemy" :
                            # 碰撞到敌人
                            if self.weapon == self.settings.hero_weapon["fist"] and \
                            self.status == self.settings.hero_status["attack"] and \
                            self.image_order >= 5 and  self.image_order <= 6 and \
                            self.direction == self.settings.hero_direction[direction] and \
                            y >= 41 and y <= 56:
                                #特殊情况 拳头部分
                                pass
                            elif self.weapon == self.settings.hero_weapon["fist"] and \
                            self.status == self.settings.hero_status["jump_attack"] and \
                            self.image_order >= 9 and  self.image_order <= 11 and \
                            self.direction == self.settings.hero_direction[direction] and \
                            y >= 95 and y <= 110:
                                pass
                            else :
                                self.get_hurt(self.settings.hero_direction[direction])

    def touch_object(self, pos, color, monster_list, tool_list):
        # 判断接触到了什么 ？ 道具, 地图, 技能, 子弹, 敌人
        (x, y) = pos
        for i in range(len(tool_list)) :
            if x >= tool_list[i].rect.left and x < tool_list[i].rect.right and \
            y >= tool_list[i].rect.top and y < tool_list[i].rect.bottom :
                if color == tool_list[i].image.get_at((x - tool_list[i].rect.left, y - tool_list[i].rect.top)):
                    name = tool_list[i].name
                    tool_list.pop(i)
                    return name
        if color == self.settings.map_color:
            # 当这个坐标在地图以下时，就是接触到地图了,有可能是一条垂直线
            if self.map.gety(self.settings.left_border + x) <= y or \
            self.map.gety(self.settings.left_border + x - 1) <= y or \
            self.map.gety(self.settings.left_border + x + 1) <= y : 
                # print("map")
                return "map"
        if self.weapon_attacks.fist_magic_firing == True :
            if x >= self.weapon_attacks.fist_magic_rect.left and x < self.weapon_attacks.fist_magic_rect.right and \
            y >= self.weapon_attacks.fist_magic_rect.top and y < self.weapon_attacks.fist_magic_rect.bottom :
                magic_pos = (x - self.weapon_attacks.fist_magic_rect.left, y - self.weapon_attacks.fist_magic_rect.top)
                if color == self.weapon_attacks.fist_magic_images[self.weapon_attacks.image_order].get_at(magic_pos):
                    return "magic"
        elif self.weapon_attacks.sword_magic_firing == True :
            if x >= self.weapon_attacks.sword_magic_rect.left and x < self.weapon_attacks.sword_magic_rect.right and \
            y >= self.weapon_attacks.sword_magic_rect.top and y < self.weapon_attacks.sword_magic_rect.bottom :
                magic_pos = (x - self.weapon_attacks.sword_magic_rect.left, y - self.weapon_attacks.fist_magic_rect.top)
                if color == self.weapon_attacks.sword_magic_images[self.weapon_attacks.image_order].get_at(magic_pos):
                    return "magic"
        # 敌人子弹
        for monster in monster_list :
            if type(monster) == MonsterPlane and monster.bullet_list:
                is_bullet = False
                image_to_del = []
                rect_to_del = []
                center_to_del = []
                dir_to_del = []
                for i in range(len(monster.bullet_list)):
                    # 如果和英雄碰撞，加入删除列表
                    if monster.bullet_alive_list[i]:
                        if x >= monster.bullet_rect_list[i].left and x < monster.bullet_rect_list[i].right and \
                                y >= monster.bullet_rect_list[i].top and y < monster.bullet_rect_list[i].bottom :
                            bullet_pos = (x - monster.bullet_rect_list[i].left, y - monster.bullet_rect_list[i].top)
                            if color == self.enemy_bullet_image.get_at(bullet_pos):
                                is_bullet = True
                                monster.bullet_alive_list[i] = False
                if is_bullet:
                    return "bullet"
        # print("enemy")
        return "enemy"

    def update_weapon_attack(self):
        self.weapon_attacks.update()
        if self.status == self.settings.hero_status["fire_magic"]:
            if self.weapon == self.settings.hero_weapon["fist"] and \
            self.image_order == self.fire_magic_size[self.weapon] - 2 and \
            self.magic_cd == 0:
                #
                self.magic -= 1
                self.magic_cd = 300
                self.weapon_attacks.image_order = 0
                # self.weapon_attacks.fist_magic_time = self.weapon_attacks.fist_magic_size
                self.weapon_attacks.fist_magic_firing = True
                if self.direction == self.settings.hero_direction["left"] :
                    self.weapon_attacks.fist_magic_rect.right = self.rect.left - 100
                elif self.direction == self.settings.hero_direction["right"] :
                    self.weapon_attacks.fist_magic_rect.left = self.rect.right + 100
                self.weapon_attacks.fist_magic_centerx = self.settings.left_border + self.weapon_attacks.fist_magic_rect.centerx
                self.weapon_attacks.fist_magic_rect.bottom = self.map.gety(self.weapon_attacks.fist_magic_centerx)
                # 初始化攻击范围
                self.weapon_attacks.fist_magic.height = 0
                self.weapon_attacks.fist_magic.width = 0
                self.weapon_attacks.fist_magic.centerx = self.weapon_attacks.fist_magic_rect.centerx
            elif self.weapon == self.settings.hero_weapon["sword"] and \
            self.image_order == self.fire_magic_size[self.weapon] - 2:
                self.magic -= 1
                self.magic_cd = 300
                self.weapon_attacks.image_order = 0
                # self.weapon_attacks.sword_magic_time = 100
                self.weapon_attacks.sword_magic_firing = True
                if self.direction == self.settings.hero_direction["left"] :
                    self.weapon_attacks.sword_magic_rect.right = self.rect.left
                elif self.direction == self.settings.hero_direction["right"] :
                    self.weapon_attacks.sword_magic_rect.left = self.rect.right
                self.weapon_attacks.sword_magic_centerx = self.settings.left_border + self.weapon_attacks.sword_magic_rect.centerx
                self.weapon_attacks.sword_magic_rect.centery = self.rect.top + 60
                self.weapon_attacks.sword_magic.height = 80
                self.weapon_attacks.sword_magic.height = 100
                self.weapon_attacks.sword_magic.center = self.weapon_attacks.sword_magic_rect.center
        elif self.status == self.settings.hero_status["attack"]:
            self.weapon_attacks.fist.width = 80
            self.weapon_attacks.fist.height = 16
            self.weapon_attacks.fist.top = self.rect.top + 41
            if self.direction == self.settings.hero_direction["left"] :
                self.weapon_attacks.fist.right = self.rect.centerx
            elif self.direction == self.settings.hero_direction["right"] :
                self.weapon_attacks.fist.left = self.rect.centerx
            self.weapon_attacks.sword["centerx"] = self.rect.centerx + 60 * self.direction
            self.weapon_attacks.sword["centery"] = self.rect.bottom - 150
            self.weapon_attacks.sword["radius"] = 85
            self.weapon_attacks.sword["direction"] = self.direction
            if self.weapon == self.settings.hero_weapon["fist"] and self.image_order >= 5 and self.image_order <= 6:
                self.weapon_attacks.fist_attacking = True
                self.weapon_attacks.sword_attacking = False
            elif self.weapon == self.settings.hero_weapon["sword"] and self.image_order >= 1 and self.image_order <= 5:
                self.weapon_attacks.fist_attacking = False
                self.weapon_attacks.sword_attacking = True
            else :
                self.weapon_attacks.fist_attacking = False
                self.weapon_attacks.sword_attacking = False
        elif self.status == self.settings.hero_status["jump_attack"]:
            self.weapon_attacks.fist.width = 80
            self.weapon_attacks.fist.height = 16
            self.weapon_attacks.fist.top = self.rect.top + 95
            if self.direction == self.settings.hero_direction["left"]:
                self.weapon_attacks.fist.right = self.rect.centerx
            elif self.direction == self.settings.hero_direction["right"]:
                self.weapon_attacks.fist.left = self.rect.centerx
            self.weapon_attacks.sword["centerx"] = self.rect.centerx + 70 * self.direction
            self.weapon_attacks.sword["centery"] = self.rect.bottom - 90
            self.weapon_attacks.sword["radius"] = 85
            self.weapon_attacks.sword["direction"] = self.direction
            if self.weapon == self.settings.hero_weapon["fist"] and self.image_order >= 9 and self.image_order <= 11:
                self.weapon_attacks.fist_attacking = True
                self.weapon_attacks.sword_attacking = False
            elif self.weapon == self.settings.hero_weapon["sword"] and self.image_order >= 8 and self.image_order <= 12:
                self.weapon_attacks.fist_attacking = False
                self.weapon_attacks.sword_attacking = True
            else :
                self.weapon_attacks.fist_attacking = False
                self.weapon_attacks.sword_attacking = False
        else :
            self.weapon_attacks.fist_attacking = False
            self.weapon_attacks.sword_attacking = False


    def update(self, monster_list, tool_list):
        self.check_collision(monster_list, tool_list)
        self.update_status()
        self.update_pos()
        self.update_weapon_attack()
        


    def change_weapon(self):
        #更换武器，什么时候适合更换武器，当该使用武器对应的动画
        self.weapon = (self.weapon + 1) % self.weapon_size
        while self.weapon_en[self.weapon] == False :
            self.weapon = (self.weapon + 1) % self.weapon_size
        if self.status == self.settings.hero_status["move"] and self.image_order >= 6: 
            self.image_order -= 6
        if self.status == self.settings.hero_status["fire_magic"] :
            self.status = self.settings.hero_status["stay"]
        if self.weapon == self.settings.hero_weapon["gun"]:
            #持枪时无攻击状态
            if self.status == self.settings.hero_status["attack"] :
                self.status = self.settings.hero_status["stay"]
            elif self.status == self.settings.hero_status["jump_attack"]:
                self.status = self.settings.hero_status["jump"]
        if self.status == self.settings.hero_status["attack"] and self.image_order >= 8:
            self.image_order = 7

    def shoot_bullet(self):
        #发射子弹
        if self.shoot_en > 0:
            #无法发射子弹
            return
        if self.direction == self.settings.hero_direction["right"]:
            bullet_velocity = self.speedx
            bullet_pos = []
            bullet_pos.append(self.rect.right + bullet_velocity)
        elif self.direction == self.settings.hero_direction["left"]:
            bullet_velocity = -self.speedx
            bullet_pos = []
            bullet_pos.append(self.rect.left + bullet_velocity)
        else :
            return 
        if self.status == self.settings.hero_status["stay"]:
            #不同状态中，枪的纵坐标不同
            bullet_pos.append(self.rect.bottom - 167)
        elif self.status == self.settings.hero_status["move"]:
            bullet_pos.append(self.rect.bottom - 175)
        elif self.status == self.settings.hero_status["jump"]:
            bullet_pos.append(self.rect.top + 40)
        else :
            return
        new_bullet = Bullet(self.screen, self.settings, bullet_pos, bullet_velocity)
        self.weapon_attacks.bullets.append(new_bullet)
        self.shoot_en = 50


    def display_frame(self, image_size):
        #播放帧
        self.frame_order += 1
        if self.frame_order >= self.frame_size:      #切换图片
            self.frame_order = 0
            self.image_order += 1
            #print(self.status, self.image_order, self.frame_order)
            if self.image_order >= image_size:
                self.image_order = 0
                if self.squating:
                    self.status = self.settings.hero_status["squat"]
                else:
                    self.status = self.settings.hero_status["stay"]

    def change_image(self, image):
        #确保切换图片后，位置没有变
        rect_centerx = self.rect.centerx
        rect_bottom = self.rect.bottom
        rect_top = self.rect.top
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = rect_centerx
        self.rect.bottom = rect_bottom
        if self.status == self.settings.hero_status["jump"] or self.status == self.settings.hero_status["jump_attack"]:
            if self.image_order == 7:
                self.rect.top = rect_top
        if self.rect.bottom > self.settings.screen_height :
            self.rect.bottom = self.settings.screen_height

    def blitme(self):
        if self.hurt_en % 6 < 3 :
            self.screen.blit(self.image, self.rect)
        self.weapon_attacks.blitme()

    def load_image_file(self, direction, weapon, images, images_path, images_size):
        #加载图片文件夹
        images[self.settings.hero_direction[direction]].append([])
        for i in range(0, images_size):
            num = str(i)
            if images_size >= 10 and i < 10:
                num = '0' + str(i)
            png_image_path = 'images/' + str(weapon) + '_' + direction + '_' + images_path + '/' + images_path + num + '.png'
            image = pygame.image.load(png_image_path)
            # image = image.convert_alpha()
            # transparent(image)
            # pygame.image.save(image, png_image_path)
            self.image_to_frame[image] = Frame(image, self.settings)
            images[self.settings.hero_direction[direction]][weapon].append(image)


    def load_images(self):
        #加载图片，图片框架
        for direction in self.settings.hero_direction.keys() :
            self.stay_images[self.settings.hero_direction[direction]] = []
            self.move_images[self.settings.hero_direction[direction]] = []
            self.attack_images[self.settings.hero_direction[direction]] = []
            self.jump_images[self.settings.hero_direction[direction]] = []
            self.jump_attack_images[self.settings.hero_direction[direction]] = []
            self.fire_magic_images[self.settings.hero_direction[direction]] = []
            self.hurt_images[self.settings.hero_direction[direction]] = []
            for weapon in range(0, self.weapon_size):
                png_image_path = 'images/' + str(weapon) + '_' + direction + '_stay.png'
                image = pygame.image.load(png_image_path)
                # image = image.convert_alpha()  
                # transparent(image)                    #背景透明化
                # pygame.image.save(image, png_image_path)
                self.image_to_frame[image] = Frame(image, self.settings)
                self.stay_images[self.settings.hero_direction[direction]].append(image)
                self.load_image_file(direction, weapon, self.move_images, 'move_images', self.move_size[weapon])
                self.load_image_file(direction, weapon, self.attack_images, 'attack_images', self.attack_size[weapon])
                self.load_image_file(direction, weapon, self.jump_images, 'jump_images', self.jump_size)
                self.load_image_file(direction, weapon, self.jump_attack_images, 'jump_attack_images', self.jump_attack_size[weapon])
                self.load_image_file(direction, weapon, self.fire_magic_images, 'fire_magic_images', self.fire_magic_size[weapon])
                self.load_image_file(direction, weapon, self.hurt_images, 'hurt_images', self.hurt_size)
                # self.squat_images[self.direction].append(pygame.image.load('game/images/' + str(weapon) + '_squat_left.jpeg')) 
                # self.load_image_file(weapon, self.squat_attack_images, 'squat_attack_images', self.squat_attack_size)
                # self.load_image_file(weapon, self.squat_move_images, 'squat_move_images', self.squat_move_size)S