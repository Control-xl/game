import pygame

class PauseMenu():
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        # self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
        # 暂停菜单的背景
        self.pause_bg = pygame.image.load('images/pause_bg_pic.png')
        # new_game按钮
        self.pause_new_game = pygame.image.load('images/pause_new_game1.png')
        # 回到主页面按钮
        self.pause_menu =  pygame.image.load('images/pause_menu1.png')
        # 新游戏字体
        self.new_game_font = pygame.font.SysFont("arial", 20)
        # 返回游戏的字体
        self.return_game_font = pygame.font.SysFont("arial", 20)
        self.new_game_rect = pygame.Rect(500, 300, 200, 100)
        self.return_game_rect = pygame.Rect(600, 400, 200, 100)

    def update(self, mouse_pst):
        if self.settings.pause:
            new_game = self.new_game_font.render("New Game", True, (0, 0, 0), (255, 255, 255))
            return_game = self.new_game_font.render("Return Game", True, (0, 0, 0), (255, 255, 255))
            self.screen.blit(new_game, self.new_game_rect)
            self.screen.blit(return_game, self.return_game_font)


    def test(self):
        self.screen.blit(self.pause_bg, (344, 208))
        self.screen.blit(self.pause_new_game, (106 + 344, 100 + 208))
        self.screen.blit(self.pause_menu, (106 + 344, 200 + 208))


