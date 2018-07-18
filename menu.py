import pygame
import sys
class Button():
    """ 按键类, 在屏幕上显示一个按键，当鼠标位于其上时，按键颜色变暗 """
    def __init__(self, screen, rect, text = "button", text_size = 16):
        self.screen = screen
        self.rect = rect
        self.state = False
        self.en_clicked = 0
        self.is_clicked = False
        font_pen = pygame.font.SysFont('arial', text_size)
        self.text = font_pen.render(text, True, (0,0,0))
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

    def blitme(self):
        self.is_clicked = False
        if self.en_clicked > 0:
            self.en_clicked -= 1
        if self.is_in_button() :
            color = (180, 180, 180)
            if pygame.mouse.get_pressed()[0]:
                color = (50, 50, 50)
                self.en_clicked = 5
            elif self.en_clicked > 0:
                self.is_clicked = True
        else :
            color = (255, 255, 255)
        radius = self.rect.height // 2
        pos = (self.rect.left+radius, self.rect.top+radius)
        pygame.draw.circle(self.screen, color, pos, radius)
        pos = (self.rect.right-radius, self.rect.top+radius)
        pygame.draw.circle(self.screen, color, pos, radius)
        rect_rect = (self.rect.x + radius, self.rect.y, self.rect.width-2*radius, self.rect.height)
        pygame.draw.rect(self.screen, color, rect_rect)
        self.screen.blit(self.text, self.text_rect)




class Menu():
    def __init__(self, screen, hero):
        self.screen = screen
        self.hero = hero
        self.occupy = False
        self.in_shop = False
        #self.button1 = pygame.image.load(r"E:\vscode\python\game\images\button1.jpg")
        self.buttons = []
        self.buttons.append(Button(self.screen, pygame.Rect(100, 60, 550, 100), "Begin game", ))
        self.buttons.append(Button(self.screen, pygame.Rect(100, 60, 550, 100), "Return game", ))
        self.buttons.append(Button(self.screen, pygame.Rect(100, 60, 550, 300), "Exit game", ))
        self.buttons.append(Button(self.screen, pygame.Rect(100, 60, 550, 200), "Shop", ))
        self.buttons.append(Button(self.screen, pygame.Rect(100, 60, 550, 100), "Sword : $100", ))
        self.buttons.append(Button(self.screen, pygame.Rect(100, 60, 550, 200), "Gun   : $500", ))
        self.buttons.append(Button(self.screen, pygame.Rect(100, 60, 550, 300), "Food  : $10", ))
        self.buttons.append(Button(self.screen, pygame.Rect(100, 60, 550, 400), "Return Menu", ))

    def update(self):
        if self.in_shop == False :
            for i in range(4):
                if self.buttons[i].is_clicked == True:
                    self.buttons[i].is_clicked = False
                    self.buttons[i].en_clicked = 0
                    if i == 2:
                        sys.exit()
                    elif i == 3:
                        self.in_shop = True
                    else :
                        self.occupy = False
        else :
            for i in range(5, 8):
                if self.buttons[i].is_clicked == True:
                    self.buttons[i].is_clicked = False
                    self.buttons[i].en_clicked = 0
                if i == 5 and self.hero.money >= 100:
                    self.hero.money -= 100
                    self.hero.weapon["sword"] = True
                if i == 5 and self.hero.money >= 100:
                    self.hero.money -= 100
                    self.hero.weapon["sword"] = True
                if i == 5 and self.hero.money >= 100:
                    self.hero.money -= 100
                    self.hero.weapon["sword"] = True
                if i == 5 and self.hero.money >= 100:
                    self.hero.money -= 100
                    self.hero.weapon["sword"] = True



    def blitme(self):
        if self.in_shop:
            for i in range(5, 8):
                self.buttons[i].blitme()
        else :
            for i in range(4):
                self.buttons[i].blitme()
