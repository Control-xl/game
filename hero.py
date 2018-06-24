import pygame
import sys
from settings import Settings
from weapon import Weapon, Bullet
from map import Map

class Frame():
    # 代表一个火柴人的外部框架，用以碰撞检测
    # 在火柴人的外表加一层白色的颜色层，当这一层东西颜色变了，发生了碰撞
    # get_at(pos)， set_at(pos, color)表示读取与设置surface中一个像素点的颜色
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.left = 0
        self.frame = [] #表示第几行的人物框架的左端和右端, 左闭右开
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
            if left > 0 :
                left -= 1
            if right < self.rect.right-1 and right != 0:
                right += 1
            self.frame.append((left, right))
            if left != right:
                self.image.set_at((left, y), (255, 255, 255, 255))
                self.image.set_at((right, y), (255, 255, 255, 255))
                self.top = min (y, self.top)
                self.bottom = max(y, self.bottom)
                self.left = min(self.left+1, left)
                self.right = max(self.right-1, right)


class Hero():
    def __init__(self, screen, map_, settings):
        self.screen = screen
        self.map = map_
        self.settings = settings
        self.frame_order = 0     #正播放的帧序号
        self.frame_size = 5      #代表一个图片要放的帧数目
        self.image_order = 0     #正播放的图片序号
        self.move_size = [6, 12, 6]       #移动图片的总数目 6,12,6
        self.attack_size = [11, 8, 0]    # 11, 11, 11
        self.jump_size = 17      # 17, 17, 17
        self.jump_attack_size = [17, 17, 0]   #17, 17, 17
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
        self.rect.bottom = self.screen.get_rect().bottom
        self.moving_left = False
        self.moving_right = False
        self.getting_hurt = False
        self.attacking = False
        self.jumping = False
        self.squating = False
        self.falling = False
        self.bullets = []
        self.shoot_en = 0                               #shoot_en = 0时才能射击
        self.speedx = 2
        self.speedy = 5
        self.velocityx = 0
        self.velocityy = -self.speedy

    def update_status(self):
        #根据旧状态即status的值继续状态;或者根据按键(即or后面)更改状态.更新image
        #可以改变方向的只有 移动键和受伤
        if self.status == self.settings.hero_status["hurt"]:
            #受伤的优先级最高, 要更新图形
            self.hurt_image()
        elif self.status == self.settings.hero_status["attack"] :
            #攻击动画
            self.attack_image()
        elif self.status == self.settings.hero_status["jump_attack"] :
            #跳起攻击动画
            self.jump_attack_image()
        elif self.status == self.settings.hero_status["squat_attack"] :
            #下蹲攻击动画
            self.squat_attack_image()
        elif self.attacking and self.weapon != self.settings.hero_weapon["gun"]:
            #当按下攻击键时，进入攻击状态
            self.attacking = False
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
        self.jumping = False
        

    def get_hurt(self, direction):
        # 发生碰撞时，调用的接口函数，
        # 更新人物方向，设置人物状态,direction表示来自左边的攻击
        # 若人物已经受伤，不再受伤
        if self.status != self.settings.hero_status["hurt"]:
            self.direction = direction
            self.status = self.settings.hero_status["hurt"]
            self.image_order = 0
            self.frame_order = 0
#播放动画
    def hurt_image(self):
        #受伤动画，播完动画则结束受伤状态
        self.velocityx = - self.direction * self.speedx
        self.velocityy = self.speedy
        self.change_image(self.hurt_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.hurt_size)

    def attack_image(self):
        #攻击动画
        self.velocityx = 0 #不变dad
        self.velocityy = self.speedy
        self.change_image(self.attack_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.attack_size[self.weapon])

    def jump_attack_image(self):
        #跳起时进行攻击
        #self.velocityx 不变
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
        #self.velocityx 不变
        if self.image_order >= 6 and self.image_order <= 7:
            self.velocityy = -self.speedy
        elif self.image_order >= 8 and self.image_order <= 10:
            self.velocityy = - self.speedy
        elif self.image_order == 11:
            self.velocityy = 0
        else :
            self.velocityy = self.speedy
        self.change_image(self.jump_images[self.direction][self.weapon][self.image_order])
        self.display_frame(self.jump_size)

    def move_image(self):
        #移动动画, 如果是状态发生改变
        self.velocityx = self.speedx * self.direction
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
        pass

    def update_herox(self):
        if self.rect.centerx > 0 and self.rect.centerx < 1200 and self.rect.bottom <= 800: #self.map.gety(self.rect.centerx + self.velocityx) :
            self.rect.centerx += self.velocityx

    def update_heroy(self):
        #跳起与坠落
        self.rect.bottom += self.velocityy
        if self.rect.bottom > 600:
            self.rect.bottom = 600
        # if self.velocityy > 0:
        #     self.rect.bottom += self.velocityy
        #     pass
        # elif self.rect.bottom < self.map.gety(self.rect.centerx):
        #     self.rect.bottom += self.velocityy
        pass


    def check_collision(self):
        #碰撞检测
        white = (255,255,255)
        frame = self.image_to_frame[self.image]
        for y in range(frame.top, frame.bottom):
            x = frame.frame[y]
            for i in range(0, len(x)):
                pos = (self.rect.left + x[i], self.rect.top + y)
                color = self.screen.get_at(pos)
                if color != (255, 255, 255, 255):
                    self.get_hurt()
                    print("hurt")


    def update(self):
        self.check_collision()
        if self.moving_left == self.moving_right:
            self.velocityx = 0
        self.update_status()
        self.update_pos()


    def change_weapon(self):
        #更换武器，什么时候适合更换武器，当该使用武器对应的动画
        self.weapon += 1
        if self.weapon == self.weapon_size:
            self.weapon = 0
        if self.status == self.settings.hero_status["move"] and self.image_order >= 6: 
            self.image_order -= 6
        if self.weapon == self.settings.hero_weapon["gun"]:
            #持枪时无攻击状态
            if self.status == self.settings.hero_status["attack"]:
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
            bullet_velocity = 0.1
            bullet_pos = []
            bullet_pos.append(self.rect.right)
        elif self.direction == self.settings.hero_direction["left"]:
            bullet_velocity = -0.1
            bullet_pos = []
            bullet_pos.append(self.rect.left)
        else :
            return 
        if self.status == self.settings.hero_status["stay"]:
            #不同状态中，枪的纵坐标不同
            bullet_pos.append(self.rect.bottom + 167)
        elif self.status == self.settings.hero_status["move"]:
            bullet_pos.append(self.rect.bottom + 175)
        elif self.status == self.settings.hero_status["jump"]:
            bullet_pos.append(self.rect.top - 40)
        else :
            return
        new_bullet = Bullet(self.screen, bullet_pos, bullet_velocity)
        self.shoot_en = 200


    def display_frame(self, image_size):
        #播放帧
        self.frame_order += 1
        if self.frame_order == self.frame_size:      #切换图片
            self.frame_order = 0
            self.image_order += 1
            if self.image_order == image_size:
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
        if self.rect.bottom > 600 :
            self.rect.bottom = 600

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def load_image_file(self, direction, weapon, images, images_path, images_size):
        #加载图片文件夹
        images[self.settings.hero_direction[direction]].append([])
        for i in range(0, images_size):
            num = str(i)
            if images_size >= 10 and i < 10:
                num = '0' + str(i)
            image_path = 'game/images/' + str(weapon) + '_' + direction + '_' + images_path + '/' + images_path + num + '.jpg'
            image = pygame.image.load(image_path)
            images[self.settings.hero_direction[direction]][weapon].append(image)
            self.image_to_frame[image] = Frame(image)

    def load_images(self):
        #加载图片，图片框架
        for direction in self.settings.hero_direction.keys() :
            self.stay_images[self.settings.hero_direction[direction]] = []
            self.move_images[self.settings.hero_direction[direction]] = []
            self.attack_images[self.settings.hero_direction[direction]] = []
            self.jump_images[self.settings.hero_direction[direction]] = []
            self.jump_attack_images[self.settings.hero_direction[direction]] = []
            self.hurt_images[self.settings.hero_direction[direction]] = []
            for weapon in range(0, self.weapon_size):
                image = pygame.image.load('game/images/' + str(weapon) + '_' + direction + '_stay.jpeg')
                self.stay_images[self.settings.hero_direction[direction]].append(image)
                self.image_to_frame[image] = Frame(image)
                self.load_image_file(direction, weapon, self.move_images, 'move_images', self.move_size[weapon])
                self.load_image_file(direction, weapon, self.attack_images, 'attack_images', self.attack_size[weapon])
                self.load_image_file(direction, weapon, self.jump_images, 'jump_images', self.jump_size)
                self.load_image_file(direction, weapon, self.jump_attack_images, 'jump_attack_images', self.jump_attack_size[weapon])
                self.load_image_file(direction, weapon, self.hurt_images, 'hurt_images', self.hurt_size)
                # self.squat_images[self.direction].append(pygame.image.load('game/images/' + str(weapon) + '_squat_left.jpeg')) 
                # self.load_image_file(weapon, self.squat_attack_images, 'squat_attack_images', self.squat_attack_size)
                # self.load_image_file(weapon, self.squat_move_images, 'squat_move_images', self.squat_move_size)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1000, 600), 0, 0)
    settings = Settings()
    map_ = Map(screen, settings)
    hero = Hero(screen, map_, settings)
    clock = pygame.time.Clock()
    while True:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    hero.get_hurt(settings.hero_direction["left"])
                if event.key == pygame.K_l:
                    hero.get_hurt(settings.hero_direction["right"])
                if event.key == pygame.K_j:
                    hero.attacking = True
                if event.key == pygame.K_w:
                    hero.jumping = True
                if event.key == pygame.K_a:
                    hero.moving_left = True
                if event.key == pygame.K_d:
                    hero.moving_right = True
                if event.key == pygame.K_s:
                    hero.squating = False
                if event.key == pygame.K_0:
                    hero.change_weapon()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    hero.moving_left = False
                if event.key == pygame.K_d:
                    hero.moving_right = False
                if event.key == pygame.K_s:
                    hero.squating = False
        screen.fill((255, 255, 255))
        hero.update()
        hero.blitme()
        pygame.display.update()