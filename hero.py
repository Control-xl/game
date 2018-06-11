import pygame
import sys
from settings import Settings
from map import Map

class Ship():

    def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载飞船图像
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 每搜飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #属性center存储小数值
        self.center = float(self.rect.centerx)

        #移动标志
        self.moving_right = False
        self.moving_left = False

        self.speed = 1

    def update(self):

        if self.moving_right and self.rect.right < self.ai_settings.screen_width/2:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.ai_settings.screen_width/10:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center


    def blitme(self):
        self.screen.blit(self.image,self.rect)


        
        
        
class Hero():
    def __init__(self, screen, map_, settings):
        self.screen = screen
        self.map = map_
        self.settings = settings
        self.frame_size = 5         #代表一个图片要放的帧数目
        self.frame_order = 0
        self.stay_right_image = pygame.image.load('game/images/stay_right.jpeg')
        self.stay_left_image = pygame.image.load('game/images/stay_left.jpeg')
        self.move_left_images = []
        self.move_right_images = []
        self.jump_right_images = []
        self.jump_left_images = []
        self.down_right_images = []
        self.down_left_images = []
        self.hurt_left_images = []
        self.hurt_right_images = []
        self.attack_left_images = []
        self.attack_right_images = []
        for i in range(1, 8):
            image_path = 'game/images/move_left_images/' + str(i) + '.jpeg'
            self.move_left_images.append(pygame.image.load(image_path))
            image_path = 'game/images/move_right_images/' + str(i) + '.jpeg'
            self.move_right_images.append(pygame.image.load(image_path))
        self.image = self.stay_right_image
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
        self.image_order = 0     #正播放的图片序号
        self.move_size = 7       #移动图片的总数目
        self.attack_size = 7
        self.jump_size = 7
        self.hurt_size = 7
        self.speedx = 1
        self.speedy = 1


    def update_image(self):
        if self.move_left_num > 0:
            #播放向左移动的动画
            self.image = self.move_left_images[self.move_left_order]
            self.frame_order += 1
            if self.frame_order == self.frame_size:      #切换图片
                self.frame_order = 0
                self.move_left_order += 1
                if self.move_left_order == self.move_left_size:
                    self.move_left_order = 0
                    self.move_left_num -= 1
                    if self.moving_left == True and self.moving_right == False:
                        self.move_left_num = 1
        elif self.move_right_num > 0:
            #播放向右移动的动画
            self.image = self.move_right_images[self.move_right_order]
            self.frame_order += 1
            if self.frame_order == self.frame_num:      #切换图片
                self.frame_order = 0
                self.move_right_order += 1
                if self.move_right_order == self.move_right_size:
                    self.move_right_order = 0
                    self.move_right_num -= 1
                    if self.moving_right == True and self.moving_left == False:
                        self.move_right_num = 1
        elif self.moving_left != self.moving_right :
            #初始化移动动画, move_left_num表示向左移动的动画的数目
            if self.moving_left:
                self.move_left_num = 1
            else :
                self.move_right_num = 1
        else :
            self.image = self.stay_right_image

    def update_status(self):
        #根据旧状态即status的值继续状态;或者根据按键(即or后面)更改状态.更新image
        #可以改变方向的只有 移动键和受伤
        if self.status == self.settings.hero_status["hurt"]:
            #受伤的优先级最高, 要更新图形
            self.hurt_image()
            pass
        elif self.status == self.settings.hero_status["attack"] or self.attacking :
            #攻击优先级次之
            self.attack_image()
            pass
        elif self.status == self.settings.hero_status["jump"] or \
             self.status == self.settings.hero_status["squat"] or \
             self.status == self.settings.hero_status["fall"] :
            # 跳跃，下蹲，掉落，第三
            pass
        elif self.jumping or self.squating or self.falling :
            #self.falling 应该改成判断self高度
            pass
        elif self.status == self.settings.hero_status["move"] or self.moving_left != self.moving_right:
            # 最后是移动
            self.move_image()
            pass
        else : #self.status == self.settings.hero_status["stay"]
            # 静止状态
            self.status

    def get_hurt(self, direction):
        # 发生碰撞时，调用的接口函数，
        # 更新人物方向，设置人物状态
        # 若人物已经受伤，不再受伤
        if self.status != self.settings.hero_status["hurt"]:
            self.direction = direction
            self.status = self.settings.hero_status["hurt"]
        pass

    def hurt_image(self):
        #受伤动画，播完动画则结束受伤状态
        pass

    def attack_image(self):
        #攻击动画
        pass

    def jump_image(self):
        #跳跃动画
        pass

    def squat_image(self):
        #下蹲动画
        pass

    def fall_image(self):
        #坠落图片
        pass

    def move_image(self):
        #移动动画, 如果是状态发生改变
        if self.status == self.settings.hero_status["move"]:
            #动画未播放完整，继续动画
            if self.direction == self.settings.hero_direction["left"]:
                self.image = self.move_left_images[self.image_order]
            elif self.direction == self.settings.hero_direction["right"]:
                self.image = self.move_left_images[self.image_order]
            self.frame_order += 1
            if self.frame_order == self.frame_size:      #切换图片
                self.frame_order = 0
                self.image_order += 1
                if self.image_order == self.move_size:
                    self.image_order = 0
                    self.status = self.settings.hero_status["stay"]
        if self.status == self.settings.hero_status["stay"] and self.moving_left != self.moving_right:
            #由stay状态变成移动状态
            self.status = self.settings.hero_status["move"]
            if self.moving_left == True:
                self.direction = self.settings.hero_direction["left"]
            elif self.moving_right == True:
                self.direction = self.settings.hero_direction["right"]


    def update_pos(self):
        self.update_herox()
        pass

    def update_herox(self):
        if self.status == self.settings.hero_status["move"] and self.direction == self.settings.hero_direction["left"] and \
           self.rect.left > 0 and self.rect.bottom <= 800: #self.map.gety(self.rect.left - self.speedx) :
            self.rect.centerx -= self.speedx
        if self.status == self.settings.hero_status["move"] and self.direction == self.settings.hero_direction["right"] and \
           self.rect.right < 1200 and self.rect.bottom <= 800: #self.map.gety(self.rect.right + self.speedx):
            self.rect.centerx += self.speedx

    def update_heroy(self):
        #跳起与坠落
        if self.status == self.settings.hero_status["jump"]:
            pass
        elif self.rect.bottom < self.map.gety(self.rect.centerx):
            self.rect.bottom += self.speedy + self.map.gety(self.rect.centerx)
        pass


    def update(self):
        self.update_status()
        self.update_pos()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), 0, 0)
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
                if event.key == pygame.K_j:
                    hero.attacking = True
                if event.key == pygame.K_w:
                    hero.jumping = True
                if event.key == pygame.K_a:
                    hero.moving_left = True
                if event.key == pygame.K_d:
                    hero.moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    hero.moving_left = False
                if event.key == pygame.K_d:
                    hero.moving_right = False
        screen.fill((255, 255, 255))
        hero.update()
        hero.blitme()
        pygame.display.update()