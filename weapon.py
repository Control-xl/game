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
        self.fist_magic_image = pygame.image.load()
        self.sword_magic_image = pygame.image.load()
        self.fist_magic_rect = self.fist_magic_image.get_rect()
        self.sword_magic_rect = self.sword_magic_image.get_rect()
        self.fist_magic = pygame.Rect(0, 0, 1, 1)
        self.sword_magic = pygame.Rect(0, 0, 1, 1)
        self.fist_magic_firing = False
        self.sword_magic_firing = False
        self.fist_magic_time = 0
        self.sword_magic_time = 0
        self.fist = pygame.Rect(0, 0, 1, 1)
        self.sword_attacking = False
        self.fist_attacking = False
    def update(self):
        if self.fist_magic_time > 0:
            self.fist_magic_time -= 1
            self.fist_magic_firing = True
        else :
            self.fist_magic_firing = False
        if self.sword_magic_time > 0 :
            self.sword_magic_time -= 1
            self.sword_magic_firing = True
        else : 
            self.sword_magic_firing = False
        for bullet in self.bullets :
            bullet.update()

    def blitme(self):
        if self.fist_magic_firing == True :
            self.screen.blit(self.fist_magic_image, self.fist_magic)
        if self.sword_magic_firing == True :
            self.screen.blit(self.sword_magic_image, self.sword_magic)
        for bullet in self.bullets : 
            bullet.blitme()


class Bullet():
    def __init__(self, screen, pos, velocity):
        self.screen = screen
        self.rect = pygame.Rect(1,1,10,10)
        self.rect.left = pos[0]
        self.rect.centery = pos[1]
        self.velocity = velocity
        self.x = float(self.rect.x)
    def update(self):
        self.x += self.velocity
        self.rect.x = self.x
    def blitme(self):
        pygame.draw.rect(self.screen, (0,0,0), self.rect)
