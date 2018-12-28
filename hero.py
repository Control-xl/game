import pygame
import sys
import math
from settings import Settings
from weapon import Weapon, Bullet
from map import Map
from monster import MonsterBall, MonsterPlane
from game_functions import transparent, play_short_music
from frame import Frame
import json


class Hero():
    def __init__(self, screen, map_, settings):
        self.screen = screen
        self.map = map_
        self.settings = settings
        self.enemy_bullet_image = pygame.image.load('images/laser/bg_bullet.png')
        self.blood_image = pygame.image.load('images/heart.ico')
        self.magic_image = pygame.image.load('images/blue_heart.png')
        self.blood_rect = self.blood_image.get_rect()
        self.magic_rect = self.magic_image.get_rect()
        self.magic_rect.top += 50
        #加载动画
        self.frame_order = 0                                                    #正播放的帧序号
        self.frame_size = 5                                                     #代表一个图片要放的帧数目
        self.basic_frame_size = 5                                               #基本帧数目
        self.jump_frame_size = [2,2,2,2,5,5,2,5, 5,10,15,25,2,2,2,2,2,]         #用于调节跳跃动作的帧数目
        #                      [0,1,2,3,4,5,6,7, 8, 9, 0, 1, 2,3,4,5,6,]
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
        self.stay_images = {}
        self.move_images = {}
        self.attack_images = {}
        self.jump_images = {}
        self.jump_attack_images = {}
        self.fire_magic_images = {}
        self.hurt_images = {}
        self.frame_num = 0                      #代表人物图片的外框的数量，等同于图片数量
        # self.squat_images = {}
        # self.squat_attack_images = {}
        # self.squat_move_images = {}
        self.image_to_frame = {}
        self.load_images()
        # for i in range(len(self.image_to_frame[self.jump_attack_images[1][0][9]].frame)):
        #     print(i, self.image_to_frame[self.jump_attack_images[1][0][9]].frame[i])
        # 初始化人物
        self.weapon = self.settings.hero_weapon["fist"]
        self.status = self.settings.hero_status["stay"]
        self.direction = self.settings.hero_direction["right"]
        self.image = self.stay_images[self.direction][self.weapon]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.settings.hero_init_centerx
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
        self.weapon_attacks = Weapon(self.screen, self.settings)
        self.weapon_en = {
            self.settings.hero_weapon["fist"] : True,
            self.settings.hero_weapon["sword"] : False,
            self.settings.hero_weapon["gun"] : False,
        }
        self.blood = 0
        self.magic = self.settings.hero_init_magic
        self.magic_level = 0
        self.magic_cd_time = 300
        self.money = 999
        self.jump_en = 1                                # 1代表可以跳跃
        self.shoot_cd = 0                               # 射击冷却时间，0时才能进行射击
        self.magic_cd = 0                               # 技能冷却时间
        self.blood_cd = 200                             # 暴血状态，非0时代表无敌
        self.speedy = 8
        self.speedx = 4
        self.velocityx = 0
        self.velocityy = -self.speedy


    def start(self):
        self.weapon = self.settings.hero_weapon["fist"]
        self.status = self.settings.hero_status["stay"]
        self.direction = self.settings.hero_direction["right"]
        self.image = self.stay_images[self.direction][self.weapon]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.settings.hero_init_centerx
        self.x = self.settings.left_border + self.rect.centerx          #在整个地图中的位置
        self.rect.bottom = self.map.gety(self.rect.centerx)
        self.blood = self.settings.hero_init_blood
        self.magic = self.settings.hero_init_magic
        self.jump_en = 1                                # 1代表可以跳跃
        self.shoot_cd = 0                               # 射击冷却时间，0时才能进行射击
        self.magic_cd = 0                               # 技能冷却时间
        self.blood_cd = 200                             # 暴血状态，非0时代表无敌
        self.speedy = 8
        self.speedx = 4
        self.velocityx = 0
        self.velocityy = -self.speedy

    def restart(self, x):
        self.x = x
        self.settings.left_border = max(int(self.x - 50), 0)
        # self.bottom = self.

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
                # self.attacking = False
                self.shoot_bullet()
        if self.shoot_cd > 0:
            self.shoot_cd -= 1
        if self.blood_cd > 0:
            self.blood_cd -= 1
        if self.magic_cd > 0:
            self.magic_cd -= 1
        if self.weapon != self.settings.hero_weapon["gun"]:
            self.attacking = False
        self.jumping = False
        self.fire_magicing = False
        

    def get_hurt(self, direction):
        # 发生碰撞时，调用的接口函数，
        # 更新人物方向，设置人物状态,direction表示攻击的来源方向
        # 若人物已经受伤，不再受伤
        if self.status != self.settings.hero_status["hurt"] and self.blood_cd == 0:
            self.direction = direction
            self.status = self.settings.hero_status["hurt"]
            self.image_order = 0
            self.frame_order = 0
            self.blood_cd = 200
            self.blood -= 1
        if self.blood <= 0 :
            pass

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
        else :
            self.velocityx = 0
        if self.image_order < 6 :
            self.velocityx = 0
        elif self.image_order >= 6 and self.image_order <= 7:
            self.velocityy = -self.speedy
        elif self.image_order >= 8 and self.image_order <= 10:
            self.velocityy = -self.speedy
        elif self.image_order == 11:
            self.velocityy = self.speedy
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
        else :
            self.velocityx = 0
        # 调节帧数目
        if self.image_order < 6 :
            self.velocityx = 0
        elif self.image_order >= 6 and self.image_order <= 7:
            self.velocityy = -self.speedy
        elif self.image_order >= 8 and self.image_order <= 10:
            self.velocityy = -self.speedy
        elif self.image_order == 11:
            self.velocityy = self.speedy
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


    # def update_pos(self):
    #     self.update_herox()
    #     self.update_heroy()

    # def update_herox(self):
    #     if self.map.gety(self.x + self.velocityx * 2) < self.rect.bottom :
    #         self.velocityx = 0
    #     if (self.x > self.settings.left_border and self.x < self.settings.left_border + self.settings.screen_width) \
    #     or (self.x <= self.settings.left_border and self.velocityx > 0)\
    #     or (self.velocityx < 0 and self.x >= self.settings.left_border + self.settings.screen_width):
    #         self.x += self.velocityx
    #         if self.settings.map_lock or \
    #         (self.velocityx > 0 and self.rect.right < self.settings.screen_width/2) or \
    #         (self.velocityx < 0 and self.rect.left > self.settings.screen_width/10):
    #             self.rect.centerx += self.velocityx
        # self.map.update(self.velocityx, self.rect)
        


    def update_herox_v2(self):
        if self.map.gety(self.x + self.velocityx * 2) < self.rect.bottom :
            self.velocityx = 0
        if (self.rect.centerx > 0 + self.speedx and self.rect.centerx < self.settings.screen_width - self.speedx) \
        or (self.rect.centerx <= self.speedx and self.velocityx > 0) \
        or (self.rect.centerx >= self.settings.screen_width - self.speedx and self.velocityx < 0):
            self.x += self.velocityx

    def update_centerx(self):
        self.rect.centerx = self.x - self.settings.left_border

    def update_heroy(self, x):
        #跳起与坠落
        self.rect.bottom += self.velocityy
        if self.rect.bottom > self.map.gety(self.x):
            self.rect.bottom = self.map.gety(self.x)
        if self.rect.bottom == self.settings.BOTTOM_NUM:
            if self.blood_cd == 0:
                self.blood -= 1
            # 重新定位
            if self.blood > 0:
                self.restart(x)
            else :
                pass
                #游戏结束
            # self.x = 50
        #print(self.x, self.rect.bottom, self.map.gety(self.x))


    def check_collision(self, monster_list, tool_list):
        #碰撞检测, 碰撞到地图, 道具, 拳头攻击到敌人, 敌人攻击
        #遇到不同颜色，先检查道具，看对应的位置的颜色是否一样，一样则是接触到了道具
        #再检测是不是正在进行拳头攻击，是的话，某些位置不会成为攻击矩形
        #否则受到攻击
        frame = self.image_to_frame[self.image]
        del_tool_list = []                                          #接触到的道具, 要在最后删除
        for y in range(frame.frame_rect["top"], frame.frame_rect["bottom"]):
            for direction, xs in frame.frame[y].items() :
                for x in xs :
                    pos = (self.rect.left + x, self.rect.top + y)
                    if pos[0] < 0 or pos[0] >= self.settings.screen_width or \
                    pos[1] < 0 or pos[1] >= self.settings.screen_height :
                        continue
                    color = self.screen.get_at(pos)
                    if color != self.settings.hero_boot_color:
                        #先检测碰撞对象
                        touch_object = self.touch_object(pos, color, monster_list, tool_list, del_tool_list)        #检测碰撞对象
                        if touch_object == "food" : #道具名称
                            self.blood += 1
                            self.blood_en = 50
                        elif touch_object == "sword" :
                            self.weapon_en["sword"] = True
                        elif touch_object == "gun" :
                            self.weapon_en["gun"] = True
                        elif touch_object == "bullet" :
                            self.get_hurt(self.settings.hero_direction[direction])
                        elif touch_object == "enemy" :
                            # 碰撞到敌人
                            if self.weapon == self.settings.hero_weapon["fist"] \
                            and self.status == self.settings.hero_status["attack"] \
                            and self.image_order >= 5 and  self.image_order <= 7 \
                            and self.direction == self.settings.hero_direction[direction] and \
                            y >= 44 and y <= 59:
                                #特殊情况 拳头部分
                                pass
                            elif self.weapon == self.settings.hero_weapon["fist"] and \
                            self.status == self.settings.hero_status["jump_attack"] and \
                            self.image_order >= 9 and  self.image_order <= 12 and \
                            self.direction == self.settings.hero_direction[direction] and \
                            y >= 97 and y <= 112:
                                pass
                            else :
                                # print(x, y, self.image_order, self.status)
                                # print(pos, pos[0]+self.settings.left_border, self.map.gety(pos[0]+self.settings.left_border)) 
                                # print(self.x, self.rect.bottom, self.map.gety(self.x))
                                self.get_hurt(self.settings.hero_direction[direction])
        for i in del_tool_list:
            tool_list.pop(i)

    def touch_object(self, pos, color, monster_list, tool_list, del_tool_list):
        # 判断接触到了什么 ？ 道具, 地图, 技能, 子弹, 敌人
        (x, y) = pos
        #检测碰撞到血槽和蓝
        if y < 50 and x < self.blood * 50 :
            return "blood"
        elif y < 100 and x < 50:
            return "blue"
        #检测道具
        for i in range(len(tool_list)) :
            if x >= tool_list[i].rect.left and x < tool_list[i].rect.right \
            and y >= tool_list[i].rect.top and y < tool_list[i].rect.bottom :
                if i in del_tool_list :
                    return "nothing"
                elif i not in del_tool_list \
                and color == tool_list[i].bg_image.get_at((x - tool_list[i].rect.left, y - tool_list[i].rect.top)):
                    name = tool_list[i].name
                    del_tool_list.append(i)
                    return name
        # 检测地图
        if color == self.settings.map_color:
            # 当这个坐标在地图以下时，就是接触到地图了,有可能是一条垂直线
            # for distance in range(-2, 3):
            #     if self.map.gety(self.settings.left_border + x + distance) <= y :
            #         return "map"
            if self.map.gety(self.settings.left_border + x - 1) <= y \
            or self.map.gety(self.settings.left_border + x) <= y \
            or self.map.gety(self.settings.left_border + x + 1) <= y : 
                return "map"
        # 检测自己的魔法
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
        # 检测敌人子弹
        for monster in monster_list :
            if type(monster) == MonsterPlane and monster.bullet_list:
                is_bullet = False
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
        # 碰撞到敌人身体
        return "enemy"

    def update_weapon_attack(self):
        self.weapon_attacks.update(self.magic_level)
        # 初始化各种攻击范围. 技能,普通攻击,跳跃攻击. (均可分为拳头和剑两种武器)
        if self.status == self.settings.hero_status["fire_magic"]:
            if self.weapon == self.settings.hero_weapon["fist"] \
            and self.image_order == self.fire_magic_size[self.weapon] - 2 \
            and self.frame_order == 0 and self.magic_cd == 0 :
                play_short_music("music/m3.wav")                                            # 播放音效
                self.magic -= 1                                                 # 扣一点蓝
                self.magic_cd = self.magic_cd_time                              # 冷却时间为300帧
                self.weapon_attacks.image_order = 0                             # 技能开始播放的帧序号
                self.weapon_attacks.fist_magic_playing = True                   # 设置技能动画播放为True
                self.weapon_attacks.fist_magic_firing = True                    # 设置技能伤害为True，命中或过时后为失效
                if self.direction == self.settings.hero_direction["left"] :     # 设置技能动画位置
                    self.weapon_attacks.fist_magic_rect.right = self.rect.left - 100
                elif self.direction == self.settings.hero_direction["right"] :
                    self.weapon_attacks.fist_magic_rect.left = self.rect.right + 100
                self.weapon_attacks.fist_magic_centerx = self.settings.left_border + self.weapon_attacks.fist_magic_rect.centerx
                self.weapon_attacks.fist_magic_rect.bottom = self.map.gety(self.weapon_attacks.fist_magic_centerx)
                if self.weapon_attacks.fist_magic_rect.bottom > self.settings.screen_height:
                    self.weapon_attacks.fist_magic_rect.bottom = self.settings.screen_height
                # 初始化攻击范围
                self.weapon_attacks.fist_magic.height = 1                       # 初始化技能伤害范围, 随动画图片变化
                self.weapon_attacks.fist_magic.width = 1
                self.weapon_attacks.fist_magic.centerx = self.weapon_attacks.fist_magic_rect.centerx
            elif self.weapon == self.settings.hero_weapon["sword"] \
            and self.image_order == self.fire_magic_size[self.weapon] - 2 \
            and self.frame_order == 0 and self.magic_cd == 0:
                play_short_music("music/m4.wav")
                self.magic -= 1
                self.magic_cd = self.magic_cd_time
                self.weapon_attacks.image_order = 0
                self.weapon_attacks.sword_magic_playing = True
                self.weapon_attacks.sword_magic_firing = True
                if self.direction == self.settings.hero_direction["left"] :
                    self.weapon_attacks.sword_magic_rect.right = self.rect.left
                elif self.direction == self.settings.hero_direction["right"] :
                    self.weapon_attacks.sword_magic_rect.left = self.rect.right
                self.weapon_attacks.sword_magic_centerx = self.settings.left_border + self.weapon_attacks.sword_magic_rect.centerx
                self.weapon_attacks.sword_magic_rect.centery = self.rect.top + 60
                self.weapon_attacks.sword_magic.height = 80
                self.weapon_attacks.sword_magic.width = 100
                self.weapon_attacks.sword_magic.center = self.weapon_attacks.sword_magic_rect.center
        elif self.status == self.settings.hero_status["attack"]:
            self.weapon_attacks.fist.width = 130
            self.weapon_attacks.fist.height = 16
            self.weapon_attacks.fist.top = self.rect.top + 44
            if self.direction == self.settings.hero_direction["left"] :
                self.weapon_attacks.fist.right = self.rect.centerx
            elif self.direction == self.settings.hero_direction["right"] :
                self.weapon_attacks.fist.left = self.rect.centerx
            self.weapon_attacks.sword["centerx"] = self.rect.centerx + 60 * self.direction
            self.weapon_attacks.sword["centery"] = self.rect.bottom - 150
            self.weapon_attacks.sword["radius"] = 85
            self.weapon_attacks.sword["direction"] = self.direction
            if self.weapon == self.settings.hero_weapon["fist"] and self.image_order >= 5 and self.image_order <= 6:
                if self.frame_order == 0 and self.image_order == 5 :                     # 初始化攻击, 命中后失效
                    self.weapon_attacks.fist_attacking = True
                    self.weapon_attacks.sword_attacking = False
            elif self.weapon == self.settings.hero_weapon["sword"] and self.image_order >= 1 and self.image_order <= 5:
                if self.frame_order == 0 and self.image_order == 1:
                    self.weapon_attacks.fist_attacking = False
                    self.weapon_attacks.sword_attacking = True
            else :
                self.weapon_attacks.fist_attacking = False
                self.weapon_attacks.sword_attacking = False
        elif self.status == self.settings.hero_status["jump_attack"]:
            self.weapon_attacks.fist.width = 110
            self.weapon_attacks.fist.height = 16
            self.weapon_attacks.fist.top = self.rect.top + 97
            if self.direction == self.settings.hero_direction["left"]:
                self.weapon_attacks.fist.right = self.rect.centerx
            elif self.direction == self.settings.hero_direction["right"]:
                self.weapon_attacks.fist.left = self.rect.centerx
            self.weapon_attacks.sword["centerx"] = self.rect.centerx + 70 * self.direction
            self.weapon_attacks.sword["centery"] = self.rect.bottom - 90
            self.weapon_attacks.sword["radius"] = 85
            self.weapon_attacks.sword["direction"] = self.direction
            if self.weapon == self.settings.hero_weapon["fist"] and self.image_order >= 9 and self.image_order <= 11:
                if self.frame_order == 0 and self.image_order == 9 :
                    self.weapon_attacks.fist_attacking = True
                    self.weapon_attacks.sword_attacking = False
            elif self.weapon == self.settings.hero_weapon["sword"] and self.image_order >= 8 and self.image_order <= 12:
                if self.frame_order == 0 and self.image_order == 8 :
                    self.weapon_attacks.fist_attacking = False
                    self.weapon_attacks.sword_attacking = True
            else :
                self.weapon_attacks.fist_attacking = False
                self.weapon_attacks.sword_attacking = False
        else :
            self.weapon_attacks.fist_attacking = False
            self.weapon_attacks.sword_attacking = False


    # def update(self, monster_list, tool_list):
    #     self.check_collision(monster_list, tool_list)
    #     self.update_status()
    #     self.update_pos()
    #     self.update_weapon_attack()



    def update1_v2(self, monster_list, tool_list):
        self.check_collision(monster_list, tool_list)
        self.update_status()
        self.update_herox_v2()

    def update2_v2(self, x):
        # 用于保证人物坐标和地图坐标同步
        self.update_centerx()
        self.update_heroy(x)
        self.update_weapon_attack()


    def change_weapon(self, weapon_order):
        #更换武器，保证更换武器后不会有动作冲突
        if self.weapon_en[weapon_order] == True:
            self.weapon = weapon_order
        # self.weapon = (self.weapon + 1) % self.weapon_size
        # while self.weapon_en[self.weapon] == False :
        #     self.weapon = (self.weapon + 1) % self.weapon_size
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
        if self.shoot_cd > 0:
            #无法发射子弹
            return
        if self.direction == self.settings.hero_direction["right"]:
            bullet_velocity = self.speedx * 2
            bullet_pos = []
            bullet_pos.append(self.rect.right + 3*self.speedx)
        elif self.direction == self.settings.hero_direction["left"]:
            bullet_velocity = -self.speedx * 2
            bullet_pos = []
            bullet_pos.append(self.rect.left - 5*self.speedx)
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
        self.shoot_cd = 50


    def display_frame(self, image_size):
        #播放帧
        self.frame_order += 1
        if self.frame_order >= self.frame_size:      #切换图片
            self.frame_order = 0
            self.image_order += 1
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
        # if self.rect.bottom > self.settings.screen_height + 300:
        #     self.rect.bottom = self.settings.screen_height + 300

    def blitme(self):
        # 绘制图片到屏幕
        if self.blood_cd % 10 < 5 :
            self.screen.blit(self.image, self.rect)
        self.weapon_attacks.blitme()
        # 绘制血条，技能冷却时间
        for i in range(self.blood):
            self.blood_rect.left = i * 50
            self.screen.blit(self.blood_image, self.blood_rect)
        if self.magic_cd == 0:
            # pygame.draw.circle(Surface, color, pos , raduis, width)
            pygame.draw.circle(self.screen, (30,30,205, 105), (25, 75), 25)
        else :
            # pygame.draw.arc(Surface, color, Rect, start_angle, stop_angle, width=1) -> Rect
            pygame.draw.arc(self.screen, (0,0,255), (0,50,50,50), 0, ((self.magic_cd)/180)*math.pi, 20)

    def load_image_file(self, direction, weapon, images, images_path, images_size):
        #加载图片文件夹
        images[self.settings.hero_direction[direction]].append([])
        for i in range(0, images_size):
            num = str(i)
            if images_size >= 10 and i < 10:
                num = '0' + str(i)
            png_image_path = 'images/' + str(weapon) + '_' + direction + '_' + images_path + '/' + images_path + num + '.png'
            image = pygame.image.load(png_image_path)
            # image = image.convert_alpha()                                 # 想要修改透明度，必须改变图片通道
            # transparent(image)                                            # 背景透明化
            # pygame.image.save(image, png_image_path)                      #
            # self.image_to_frame[image] = Frame(image, self.settings)      # 描绘人物外框,并对人物图片进行修改
            # pygame.image.save(image, png_image_path)                      # 保存图片
            # frame = Frame(image, self.settings)                           # 
            frame_path = "frames/frame/"+str(self.frame_num) + ".txt"
            frame_rect_path = "frames/frame_rect/" + str(self.frame_num) + ".txt"
            self.frame_num += 1
            # with open(frame_path,'w') as file_obj:                        # 将人物外框事先保存在json文件中
            #     file_obj.write(json.dumps(frame.frame))                   # 这样就不用每次开启的时候都要描绘外框
            # with open(frame_rect_path,'w') as file_obj:                   # 减少开启的时间
            #     file_obj.write(json.dumps(frame.frame_rect))              #
            with open(frame_path,'r') as file_obj:
                frame_frame = json.loads(file_obj.read())
            with open(frame_rect_path,'r') as file_obj:
                frame_frame_rect = json.loads(file_obj.read())
            self.image_to_frame[image] = Frame(image, self.settings, True, frame_frame, frame_frame_rect)
            images[self.settings.hero_direction[direction]][weapon].append(image)


    def load_images(self):
        #加载图片，图片人物框架
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
                # image = image.convert_alpha()                                 #
                # transparent(image)                                            # 背景透明化
                # pygame.image.save(image, png_image_path)                      #
                # self.image_to_frame[image] = Frame(image, self.settings)      # 描绘人物外框
                # pygame.image.save(image, png_image_path)                      # 保存图片
                # frame = Frame(image, self.settings)                           # 
                frame_path = "frames/frame/"+str(self.frame_num) + ".txt"
                frame_rect_path = "frames/frame_rect/" + str(self.frame_num) + ".txt"
                self.frame_num += 1
                # with open(frame_path,'w') as file_obj:                        # 将人物外框事先保存在json文件中
                #     file_obj.write(json.dumps(frame.frame))                   # 这样就不用每次开启的时候都要描绘外框
                # with open(frame_rect_path,'w') as file_obj:                   # 减少开启的时间
                #     file_obj.write(json.dumps(frame.frame_rect))
                with open(frame_path,'r') as file_obj:
                    frame_frame = json.loads(file_obj.read())
                with open(frame_rect_path,'r') as file_obj:
                    frame_frame_rect = json.loads(file_obj.read())
                self.image_to_frame[image] = Frame(image, self.settings, True, frame_frame, frame_frame_rect)
                self.stay_images[self.settings.hero_direction[direction]].append(image)
                self.load_image_file(direction, weapon, self.move_images, 'move_images', self.move_size[weapon])
                self.load_image_file(direction, weapon, self.attack_images, 'attack_images', self.attack_size[weapon])
                self.load_image_file(direction, weapon, self.jump_images, 'jump_images', self.jump_size)
                self.load_image_file(direction, weapon, self.jump_attack_images, 'jump_attack_images', self.jump_attack_size[weapon])
                self.load_image_file(direction, weapon, self.fire_magic_images, 'fire_magic_images', self.fire_magic_size[weapon])
                self.load_image_file(direction, weapon, self.hurt_images, 'hurt_images', self.hurt_size)
                # self.squat_images[self.direction].append(pygame.image.load('game/images/' + str(weapon) + '_squat_left.jpeg')) 
                # self.load_image_file(weapon, self.squat_attack_images, 'squat_attack_images', self.squat_attack_size)
                # self.load_image_file(weapon, self.squat_move_images, 'squat_move_images', self.squat_move_size)


if __name__ == '__main__':
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), 0, 0)
    map_ = Map(screen, settings)
    tool_list = []
    hero = Hero(screen, map_, settings)
    # tool = Tool(screen, settings, "food", (600, 700))
    # tool_list.append(tool)
    monster_list = []
    clock = pygame.time.Clock()
    while True:
        clock.tick(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        hero.update(monster_list, tool_list)
        map_.update(hero, monster_list)
        screen.fill(settings.bg_color)
        hero.blitme()
        map_.blitme()
        pygame.display.update()