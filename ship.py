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
        self.blood = self.ai_settings.hero_init_blood

    def update(self):

        if self.moving_right and self.rect.right < self.ai_settings.screen_width/2:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.ai_settings.screen_width/10:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.center


    def blitme(self):
        self.screen.blit(self.image,self.rect)

