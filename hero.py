import pygame


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
    def __init__(self, screen, map_):
        self.screen = screen
        self.map = map_
        self.frame_num = 10
        self.frame_order = 0
        self.stay_image = pygame.image.load('game/images/stay.jpeg')
        self.move_left_images = []
        self.move_right_images = []
        self.up_images = []
        self.down_images = []
        for i in range(1, 8):
            image_path = 'game/images/move_left_images/' + str(i) + '.jpeg'
            self.move_left_images.append(pygame.image.load(image_path))
            image_path = 'game/images/move_right_images/' + str(i) + '.jpeg'
            self.move_right_images.append(pygame.image.load(image_path))
        self.image = self.stay_image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen.get_rect().centerx
        self.rect.bottom = self.screen.get_rect().bottom
        self.moving_left = False
        self.move_left_order = 0
        self.move_left_num = 0
        self.move_left_size = 7
        self.moving_right = False
        self.move_right_order = 0
        self.move_right_num = 0
        self.move_right_size = 7
        self.speedx = 1
        self.speedy = 1
        self.hurt_time = 0
        self.jump = 0
        self.attack = 0

    def update_image(self):
        if self.attack > 0:
            #攻击
            self.image = self.attack_image
            self.attack -= 1
        elif self.jump > 0:
            #跳跃
            if self.jump % 50 == 0 and self.jump > 250:
                #self.image = self.jump_image
                self.rect.bottom -= 10
            elif self.jump % 50 == 0:
                #self.image = self.jump_image
                self.rect.bottom += 10
            self.jump -= 1
        elif self.move_left_num > 0:
            #播放向左移动的动画
            self.image = self.move_left_images[self.move_left_order]
            self.frame_order += 1
            if self.frame_order == self.frame_num:      #切换图片
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
            self.image = self.stay_image

    def update_pos(self):
        if self.moving_left:
            self.rect.centerx -= self.speedx
        if self.moving_right:
            self.rect.centerx += self.speedx

    def move_x(self):
        if self.moving_left and self.rect.left > 0 and self.rect.bottom <= 800: #self.map.get_y(self.rect.left - self.speed) :
            self.rect.centerx -= self.speedx
        if self.moving_right and self.rect.right < 1200 and self.rect.bottom <= 800:# self.map.get_y(self.rect.right + self.speed):
            self.rect.centerx += self.speedx

    def move_y(self):
        #跳起与坠落
        pass

    def get_hurt(self, direction):
        pass

    def attack(self):
        pass

    def jump():
        pass

    def hurt_image(self):
        #受伤动画
        pass

    def attack_image(self):
        #攻击动画
        pass

    def jump_image(self):
        #跳跃动画
        pass

    def down_image(self):
        #坠落图片
        pass

    def update(self):
        self.update_image()
        self.move_x()

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
