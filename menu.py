import pygame
import sys


class Button():
    """ 按键类, 在屏幕上显示一个按键，当鼠标位于其上时，按键颜色变暗 """
    def __init__(self, screen, rect, text_message = "button", text_size = 16):
        self.screen = screen
        self.rect = rect
        self.state = False
        self.en_clicked = 0
        self.is_clicked = False
        self.text_size = text_size
        self.font_pen = pygame.font.SysFont('arial', self.text_size)
        self.text_message = text_message
        self.text = self.font_pen.render(self.text_message, True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.rect.centerx
        self.text_rect.centery = self.rect.centery

    def is_in_button(self):
        mousex, mousey = pygame.mouse.get_pos()
        radius = self.rect.height // 2
        pos = (self.rect.left+radius, self.rect.top+radius)
        if (mousex - pos[0])**2 + (mousey - pos[1])**2 <= radius ** 2:
            return True
        pos = (self.rect.right-radius, self.rect.top+radius)
        if (mousex - pos[0])**2 + (mousey - pos[1])**2 <= radius ** 2:
            return True
        if mousex < self.rect.left or mousex > self.rect.right:
            return False
        elif mousey < self.rect.top or mousey > self.rect.bottom:
            return False
        else :
            return True

    def update_text(self, text_message):
        self.text_message = text_message
        self.text = self.font_pen.render(self.text_message, True, (0,0,0))
        self.text_rect = self.text.get_rect()
        self.text_rect.centerx = self.rect.centerx
        self.text_rect.centery = self.rect.centery

    def blitme(self):
        self.is_clicked = False
        if self.en_clicked > 0:
            self.en_clicked -= 1
        if self.is_in_button() :
            color = (120, 120, 120)
            if pygame.mouse.get_pressed()[0]:
                color = (50, 50, 50)
                self.en_clicked = 5
            elif self.en_clicked > 0:
                self.is_clicked = True
        else :
            color = (200, 200, 200)
        radius = self.rect.height // 2
        pos = (self.rect.left+radius, self.rect.top+radius)
        pygame.draw.circle(self.screen, color, pos, radius)
        pos = (self.rect.right-radius, self.rect.top+radius)
        pygame.draw.circle(self.screen, color, pos, radius)
        rect_rect = (self.rect.x + radius, self.rect.y, self.rect.width-2*radius, self.rect.height)
        pygame.draw.rect(self.screen, color, rect_rect)
        self.screen.blit(self.text, self.text_rect)


class Menu():
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.occupy = False
        self.in_shop = False
        self.text_size = 30
        self.font_pen = pygame.font.SysFont('arial', self.text_size)
        self.menu_text_message = "Menu"
        self.menu_text = self.font_pen.render(self.menu_text_message, True, (0,0,0))
        self.menu_text_rect = self.menu_text.get_rect()
        self.menu_text_rect.centerx = 600
        self.menu_text_rect.top = 100
        self.shop_text_message = "$0"
        self.shop_text = self.font_pen.render(self.shop_text_message, True, (0,0,0))
        self.shop_text_rect = self.shop_text.get_rect()
        self.shop_text_rect.centerx = 600
        self.shop_text_rect.top = 100
        self.money = 0
        #self.button1 = pygame.image.load(r"E:\vscode\python\game\images\button1.jpg")
        self.buttons = []
        button_size = (160, 60)
        self.buttons.append(Button(self.screen, pygame.Rect((520, 150), button_size), "Begin game", ))
        self.buttons.append(Button(self.screen, pygame.Rect((520, 150), button_size), "Return game", ))
        self.buttons.append(Button(self.screen, pygame.Rect((520, 230), button_size), "Exit game", ))
        self.buttons.append(Button(self.screen, pygame.Rect((520, 310), button_size), "Shop", ))
        self.buttons.append(Button(self.screen, pygame.Rect((520, 150), button_size), "Sword : 100", ))
        self.buttons.append(Button(self.screen, pygame.Rect((520, 230), button_size), "Gun : 500", ))
        self.buttons.append(Button(self.screen, pygame.Rect((520, 310), button_size), "Food : 10", ))
        self.buttons.append(Button(self.screen, pygame.Rect((520, 390), button_size), "Level 1: 50", ))
        self.buttons.append(Button(self.screen, pygame.Rect((520, 470), button_size), "Return Menu", ))

    def update(self, hero, map_, monster_list):
        if self.money != hero.money:
            self.shop_text_message = str(self.money)
            self.shop_text_rect = self.shop_text.get_rect()
            self.shop_text_rect.centerx = 600
            self.shop_text_rect.top = 100
        if self.in_shop == False :
            for i in range(4):
                if self.buttons[i].is_clicked == True:
                    self.buttons[i].is_clicked = False
                    self.buttons[i].en_clicked = 0
                    if i == 0:
                        self.occupy = False
                        self.settings.__init__()
                        hero.start()
                        map_.__init__(self.screen, self.settings)
                        monster_list.clear()
                    elif i == 1:
                        self.occupy = False
                    elif i == 2:
                        sys.exit()
                    elif i == 3:
                        self.in_shop = True
        else :
            for i in range(4, 9):
                if self.buttons[i].is_clicked == True:
                    self.buttons[i].is_clicked = False
                    self.buttons[i].en_clicked = 0
                    if i == 4 and hero.money >= 100:
                        hero.money -= 100
                        hero.weapon["sword"] = True
                    if i == 5 and hero.money >= 500:
                        hero.money -= 100
                        hero.weapon["gun"] = True
                    if i == 6 and hero.money >= 10:
                        hero.money -= 10
                        hero.blood += 1
                    if i == 7 and hero.money >= 50:
                        hero.money -= 50
                        hero.magic_level += 1
                        if hero.magic_level < 5:
                            self.buttons[i].update_text("Level " + str(hero.magic_level + 1) + ": 50")
                    if i == 8 :
                        self.in_shop = False



    def blitme(self, hero):
        color = (230, 230, 230, 15)
        rect = (450, 50, 300, 500)
        pygame.draw.rect(self.screen, color, rect)
        if self.in_shop:
            self.screen.blit(self.shop_text, self.shop_text_rect)
            for i in range(4, 9):
                self.buttons[i].blitme()
        else :
            self.screen.blit(self.menu_text, self.menu_text_rect)
            if hero.blood > 0:
                self.buttons[1].blitme()
            else:
                self.buttons[0].blitme()
            for i in range(2,4):
                self.buttons[i].blitme()
