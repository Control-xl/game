import pygame
import sys
from settings import Settings
from map import Map

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
        self.weapon_size = 3#self.settings.hero_weapon_size
        self.stay_right_images = []
        self.stay_left_images = []
        self.move_left_images = []
        self.move_right_images = []
        self.attack_left_images = []
        self.attack_right_images = []
        self.jump_right_images = []
        self.jump_left_images = []
        self.jump_attack_left_images = []
        self.jump_attack_right_images = []
        self.hurt_left_images = []
        self.hurt_right_images = []
        self.squat_left_images = []
        self.squat_right_images = []
        self.squat_attack_left_images = []
        self.squat_attack_right_images = []
        self.squat_move_left_images = []
        self.squat_move_right_images = []
        self.fall_right_images = []
        self.fall_left_images = []
        self.load_images()
        self.weapon = self.settings.hero_weapon["fist"]
        self.image = self.stay_right_images[self.weapon]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.bottom = self.screen.get_rect().bottom
        self.status = settings.hero_status["stay"]
        self.direction = settings.hero_direction["right"]
        self.moving_left = False
        self.moving_right = False
        self.getting_hurt = False
        self.attacking = False
        self.jumping = False
        self.squating = False
        self.falling = False
        self.bullets = []
        self.speedx = 2
        self.speedy = 1
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
            """
        elif self.status == self.settings.hero_status["fall"] :
            # 掉落，第三
            pass
            """
        elif self.status == self.settings.hero_status["squat_move"]:
            #蹲着移动
            self.squat_move()
        elif self.squating :
            #下蹲键, 按着蹲下键时，无法跳跃，即按跳起键无效。当此时有移动按键时，将变成蹲着移动
            self.status = self.settings.hero_status["squat"]
            self.squat_image()
        elif self.jumping :
            #跳跃键
            self.status = self.settings.hero_status["jump"]
            """
        elif self.falling :
            #self.falling 应该改成判断self高度
            pass
            """
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

    def hurt_image(self):
        #受伤动画，播完动画则结束受伤状态
        self.velocityx = - self.direction * self.speedx
        self.velocityy = self.speedy
        if self.direction == self.settings.hero_direction["left"]:
            self.image = self.hurt_left_images[self.weapon][self.image_order]
        elif self.direction == self.settings.hero_direction["right"]:
            self.image = self.hurt_right_images[self.weapon][self.image_order]
        self.display_frame(self.hurt_size)

    def attack_image(self):
        #攻击动画
        self.velocityx = 0 #不变dad
        self.velocityy = self.speedy
        if self.direction == self.settings.hero_direction["left"]:
            self.change_image(self.attack_left_images[self.weapon][self.image_order])
        elif self.direction == self.settings.hero_direction["right"]:
            self.change_image(self.attack_right_images[self.weapon][self.image_order])
        self.display_frame(self.attack_size[self.weapon])

    def jump_attack_image(self):
        #跳起时进行攻击
        #self.velocityx 不变
        if self.image_order >= 6 and self.image_order <= 7:
            self.velocityy = -3
        elif self.image_order >= 8 and self.image_order <= 10:
            self.velocityy = -6
        elif self.image_order == 11:
            self.velocityy = 0
        else :
            self.velocityy = 5
        if self.direction == self.settings.hero_direction["left"]:
            self.change_image(self.jump_attack_left_images[self.weapon][self.image_order])
        elif self.direction == self.settings.hero_direction["right"]:
            self.change_image(self.jump_attack_right_images[self.weapon][self.image_order])
        self.display_frame(self.jump_attack_size[self.weapon])

    def jump_image(self):
        #跳跃动画
        #self.velocityx 不变
        if self.image_order >= 6 and self.image_order <= 10:
            self.velocityy = -5
        elif self.image_order == 11:
            self.velocityy = 0
        else :
            self.velocityy = 5
        if self.direction == self.settings.hero_direction["left"]:
            self.change_image(self.jump_left_images[self.weapon][self.image_order]) 
        elif self.direction == self.settings.hero_direction["right"]:
            self.change_image(self.jump_right_images[self.weapon][self.image_order])
        self.display_frame(self.jump_size)

    def move_image(self):
        #移动动画, 如果是状态发生改变
        self.velocityx = self.speedx * self.direction
        self.velocityy = self.speedy
        #动画未播放完整，继续动画
        if self.direction == self.settings.hero_direction["left"]:
            self.change_image(self.move_left_images[self.weapon][self.image_order])
        elif self.direction == self.settings.hero_direction["right"]:
            self.change_image(self.move_right_images[self.weapon][self.image_order])
        self.display_frame(self.move_size[self.weapon])

    def stay_image(self):
        if self.direction == self.settings.hero_direction["left"]:
            self.change_image(self.stay_left_images[self.weapon])
        elif self.direction == self.settings.hero_direction["right"]:
            self.change_image(self.stay_right_images[self.weapon])

    def fall_image(self):
        #坠落图片
        pass

    def squat_image(self):
        #下蹲动画,有方向时变成滚动了
        if self.moving_left != self.moving_right :
            self.status = self.settings.hero_status["squat_move"]
            if self.moving_left == True:
                self.direction = self.settings.hero_direction["left"]
            elif self.moving_right == True:
                self.direction = self.settings.hero_direction["right"]
        elif self.direction == self.settings.hero_direction["left"]:
            self.change_image(self.squat_left_image)
        elif self.direction == self.settings.hero_direction["right"]:
            self.change_image(self.squat_right_image)

    def squat_move(self):
        self.velocityx = 2 * self.speedx * self.direction
        self.velocityy = -self.speedy
        #动画未播放完整，继续动画
        if self.direction == self.settings.hero_direction["left"]:
            self.change_image(self.squat_move_left_images[self.weapon][self.image_order])
        elif self.direction == self.settings.hero_direction["right"]:
            self.change_image(self.squat_move_right_images[self.weapon][self.image_order])
        self.display_frame(self.squat_move_size)

    def squat_attack_image(self):
        if self.direction == self.settings.hero_direction["left"]:
            self.change_image(self.squat_attack_left_images[self.weapon][self.image_order])
        elif self.direction == self.settings.hero_direction["right"]:
            self.change_image(self.squat_attack_right_images[self.weapon][self.image_order])
        self.display_frame(self.squat_attack_size)

    def update_pos(self):
        self.update_herox()
        self.update_heroy()
        pass

    def update_herox(self):
        if self.rect.centerx > 0 and self.rect.centerx < 1200 and self.rect.bottom <= 800: #self.map.gety(self.rect.centerx + self.velocityx) :
            self.rect.centerx += self.velocityx
            """
        if self.status == self.settings.hero_status["move"] and self.direction == self.settings.hero_direction["left"] and \
           self.rect.left > 0 and self.rect.bottom <= 800: #self.map.gety(self.rect.left - self.speedx) :
            self.rect.centerx -= self.speedx
        if self.status == self.settings.hero_status["move"] and self.direction == self.settings.hero_direction["right"] and \
           self.rect.right < 1200 and self.rect.bottom <= 800: #self.map.gety(self.rect.right + self.speedx):
            self.rect.centerx += self.speedx
            """

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

    def update(self):
        if self.moving_left == self.moving_right:
            self.velocityx = 0
        self.update_status()
        self.update_pos()

    def display_frame(self, image_size):
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

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def shoot_bullet(self):
        #发射子弹
        if self.status == self.settings.hero_status["jump"]:
            pass
        elif self.status == self.settings.hero_status["jump_attack"]:
            pass
        else :
            pass

    def change_weapon(self):
        self.weapon += 1
        if self.weapon == self.weapon_size:
            self.weapon = 0
        if self.weapon == self.settings.hero_weapon["gun"]:
            #持枪时无攻击状态
            if self.status == self.settings.hero_status["attack"]:
                self.status = self.settings.hero_status["stay"]
            elif self.status == self.settings.hero_status["jump_attack"]:
                self.status = self.settings.hero_status["jump"]

    def get_attack_rect(self):
        pass

    def get_body_rect(self):
        pass

    def load_image_file(self, weapon, images, images_path, images_size):
        images.append([])
        for i in range(0, images_size):
            num = str(i)
            if images_size >= 10 and i < 10:
                num = '0' + str(i)
            image_path = 'game/images/' + str(weapon) + images_path + num + '.jpg'
            images[weapon].append(pygame.image.load(image_path))

    def load_images(self):
        #加载图片
        for weapon in range(0, self.weapon_size):
            self.stay_right_images.append(pygame.image.load('game/images/' + str(weapon) + '_stay_right.jpeg'))
            self.stay_left_images.append(pygame.image.load('game/images/' + str(weapon) + '_stay_left.jpeg'))
            self.load_image_file(weapon, self.move_left_images, '_move_left_images/move_images', self.move_size[weapon])
            self.load_image_file(weapon, self.move_right_images, '_move_right_images/move_images', self.move_size[weapon])
            self.load_image_file(weapon, self.attack_left_images, '_attack_left_images/attack_images', self.attack_size[weapon])
            self.load_image_file(weapon, self.attack_right_images, '_attack_right_images/attack_images', self.attack_size[weapon])
            self.load_image_file(weapon, self.jump_left_images, '_jump_left_images/jump_images', self.jump_size)
            self.load_image_file(weapon, self.jump_right_images, '_jump_right_images/jump_images', self.jump_size)
            self.load_image_file(weapon, self.jump_attack_left_images, '_jump_attack_left_images/jump_attack_images', self.jump_attack_size[weapon])
            self.load_image_file(weapon, self.jump_attack_right_images, '_jump_attack_right_images/jump_attack_images', self.jump_attack_size[weapon])
            self.load_image_file(weapon, self.hurt_left_images, '_hurt_left_images/hurt_images', self.hurt_size)
            self.load_image_file(weapon, self.hurt_right_images, '_hurt_right_images/hurt_images', self.hurt_size)
            # self.squat_left_images.append(pygame.image.load('game/images/' + str(weapon) + '_squat_left.jpeg')) 
            # self.squat_right_images.append(pygame.image.load('game/images/' + str(weapon) + '_squat_right.jpeg'))
            # self.load_image_file(weapon, self.squat_attack_left_images, '_squat_attack_left_images/squat_attack_images_', self.squat_attack_size)
            # self.load_image_file(weapon, self.squat_attack_right_images, '_squat_attack_right_images/squat_attack_images_', self.squat_attack_size)
            # self.load_image_file(weapon, self.squat_move_left_images, '_squat_move_left_images/squat_move_images_', self.squat_move_size)
            # self.load_image_file(weapon, self.squat_move_right_images, '_squat_move_right_images/squat_move_images_', self.squat_move_size)



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