import pygame
class Weapon():
    # 维护hero释放的物理攻击，魔法攻击
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.bullets = []
        self.sword = {
            "centerx": 0,
            "centery": 0,
            "radius": 0,
            "direction" : self.settings.hero_direction["right"]
        }
        self.fist = pygame.Rect(0, 0, 1, 1)
        self.sword_attacking = False
        self.fist_attacking = False
        self.fist_magic_damage = 5
        self.fist_magic_damage = 5
        self.fist_magic = pygame.Rect(0, 0, 1, 1)
        self.fist_magic_width = 60
        self.fist_magic.width = self.fist_magic_width
        self.sword_magic = pygame.Rect(0, 0, 1, 1)
        self.sword_magic.width = 100
        self.sword_magic.height = 80
        self.fist_magic_firing = False
        self.sword_magic_firing = False
        self.image_order = 0
        self.frame_order = 0
        self.frame_size = 5
        self.fist_magic_images = []
        self.fist_magic_size = 8
        for i in range(1, self.fist_magic_size + 1):
            image = pygame.image.load('images/magics/fist/' + str(i) + '.png')
            self.fist_magic_images.append(image)
        self.fist_magic_rect = self.fist_magic_images[0].get_rect()
        self.fist_magic_centerx = self.fist_magic_rect.centerx
        self.sword_magic_images = []
        self.sword_magic_size = 8
        for i in range(1, self.sword_magic_size + 1):
            image = pygame.image.load('images/magics/sword/' + str(i) + '.png')
            self.sword_magic_images.append(image)
        self.sword_magic_rect = self.sword_magic_images[0].get_rect()
        self.sword_magic_centerx = self.sword_magic_rect.centerx
        self.fist_magic_time = 0
        self.sword_magic_time = 0

    def update(self):
        # 更新子弹, 技能位置, image_order
        if self.fist_magic_firing == True :
            self.frame_order += 1
            if self.frame_order >= self.frame_size :
                self.frame_order = 0
                self.image_order += 1
                if self.image_order >= self.fist_magic_size :
                    self.image_order = 0
                    self.fist_magic_firing = False
            # 根据image_order 改变 攻击范围
            if self.image_order < 1  or self.image_order >= self.fist_magic_size - 1:
                self.fist_magic.height = 0
            elif self.image_order == 1 :
                self.fist_magic.height = 200
                self.fist_magic.top = self.fist_magic_rect.top
            elif self.image_order == 2 :
                self.fist_magic.height = 390
                self.fist_magic.top = self.fist_magic_rect.top
            elif self.image_order >= 3 and self.image_order <= 4 :
                self.fist_magic.height = self.fist_magic_rect.height
            elif self.image_order == 5 :
                self.fist_magic.height = 385
                self.fist_magic.bottom = self.fist_magic_rect.bottom
            elif self.image_order == 6 :
                self.fist_magic.height = 60
                self.fist_magic.bottom = self.fist_magic_rect.bottom
            self.fist_magic.width = self.fist_magic_width
            self.fist_magic_rect.centerx = self.fist_magic_centerx - self.settings.left_border
            self.fist_magic.centerx = self.fist_magic_rect.centerx
            print(self.image_order, self.fist_magic, self.fist_magic_rect)
        else :
            self.fist_magic_firing = False
        if self.sword_magic_firing == True :
            self.frame_order += 1
            if self.frame_order >= self.frame_size :
                self.frame_order = 0
                self.image_order += 1
                if self.image_order >= self.sword_magic_size :
                    self.image_order = 0
                    self.sword_magic_firing = False
                # 根据image_order 改变 攻击范围
            if self.image_order < 0  or self.image_order >= self.fist_magic_size - 2:
                self.sword_magic.height = 0
                self.sword_magic.width = 0
            elif self.image_order >= 0 and self.image_order <= 3 :
                self.sword_magic.height = 80
                self.sword_magic.width = 100
            elif self.image_order >= 4 and self.image_order <= 5 :
                self.sword_magic.height = 80
                self.sword_magic.width = 100
            self.sword_magic_rect.centerx = self.sword_magic_centerx - self.settings.left_border
            self.sword_magic.center = self.sword_magic_rect.center
        else : 
            self.sword_magic_firing = False
        i = len(self.bullets)
        while i > 0 :
            i -= 1
            if self.bullets[i].rect.right < 0 or self.rect.left > self.settings.screen_width :
                self.bullets.pop(i)
            else :
                self.bullets[i].update()

    def blitme(self):
        if self.fist_magic_firing == True :
            self.screen.blit(self.fist_magic_images[self.image_order], self.fist_magic_rect)
        if self.sword_magic_firing == True :
            self.screen.blit(self.sword_magic_image, self.sword_magic_rect)
        for bullet in self.bullets : 
            bullet.blitme()


class Bullet():
    def __init__(self, screen, settings, pos, velocity):
        self.screen = screen
        self.settings = settings
        self.rect = pygame.Rect(1,1,10,10)
        self.rect.left = pos[0]
        self.rect.centery = pos[1]
        self.velocity = velocity
        self.x = float(self.rect.x) + self.settings.left_border
    def update(self):
        self.x += self.velocity
        self.rect.x = self.x - self.settings.left_border
    def blitme(self):
        pygame.draw.rect(self.screen, (0,0,0), self.rect)