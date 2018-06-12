import pygame


class StateDisplay():

    def __init__(self, screen, settings):
        self.settings = settings
        self.screen = screen
        # 设置显示的血量
        self.blood = settings.hero_init_blood
        self.blood_ico = pygame.image.load('images/heart.ico')
        self.blood_ico.convert()
        self.blood_rect = self.blood_ico.get_rect()
        self.blood_ico_list = []
        for i in range(self.blood):
            self.blood_ico_list.append(self.blood_ico)

        # 设置蓝量
        self.magic = settings.hero_init_magic

        # 设置图标位置



    def update(self, hero):
        self.blood = hero.blood
        length = len(self.blood_ico_list)
        if self.blood > length:
            for i in range(self.blood - length):
                self.blood_ico_list.append(self.blood_ico)


    def blitme(self):

        for i in range(self.blood):
            self.screen.blit(self.blood_ico_list[i],
                             (i * self.blood_rect.width, 0))
