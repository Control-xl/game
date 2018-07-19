import pygame
import sys
import threading

def check_keydown_events(event, settings, screen, hero, menu):
    if event.key == pygame.K_ESCAPE :
        menu.occupy = True
    if event.key == pygame.K_k:
        hero.fire_magicing = True
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
    if event.key == pygame.K_1:
        hero.change_weapon(0)
    if event.key == pygame.K_2:
        hero.change_weapon(1)
    if event.key == pygame.K_3:
        hero.change_weapon(2)
        
    # if event.key == pygame.K_ESCAPE:
    #     if settings.pause:
    #         settings.pause = False
    #     else:
    #         settings.pause = True

    #     print(settings.pause)
    #     return
    # if event.key == pygame.K_RIGHT:
    #      # 右移
    #     hero.moving_right = True
    # if event.key == pygame.K_LEFT:
    #     # left移
    #     hero.moving_left = True
    # if event.key == pygame.K_DOWN:
    #     hero.blood -= 1
    # if event.key == pygame.K_UP:
    #     hero.blood += 1


def check_keyup_events(event, hero):
    if event.key == pygame.K_k:
        hero.fire_magicing = False
    if event.key == pygame.K_j:
        hero.attacking = False
    if event.key == pygame.K_a:
        hero.moving_left = False
    if event.key == pygame.K_d:
        hero.moving_right = False
    if event.key == pygame.K_s:
        hero.squating = False


def check_events(settings, screen, hero, menu):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, hero, menu)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, hero)


def update_screen(settings, screen, background_pic,hero, map1, state_display, pause_menu,
                  monster_ball, monster_plane):
    screen.fill(settings.bg_color)
    if not settings.pause:
        background_pic.set_alpha(255)
        hero.blitme()
        map1.blitme()
        state_display.blitme()
        monster_ball.blitme()
        monster_plane.blitme()
    else:
        # 使得飞机、地图和状态元素仍然得到显示
        hero.blitme()
        map1.blitme()
        state_display.blitme()
        monster_ball.blitme()
        monster_plane.blitme()

        # 灰色元素
        screen.blit(background_pic, (0, 0))
        pause_menu.test()
        background_pic.set_alpha(150)


def play_short_music(music_name,  volume = 0.1, loops = 0):
    """播放短效音乐，比如击中 等效果，建议以ogg结尾"""
    music = pygame.mixer.Sound(music_name)
    music.set_volume(volume)
    music.play(loops)


def play_bg_music(music_name, loops=-1, volume = 0.1):
    """播放背景音乐，MP3格式"""
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops)


def transparent(image, exp_r = 200, exp_g = 200, exp_b = 200, comp = 1):
    #将背景改为透明背景
    rect = image.get_rect()
    for x in range(rect.left, rect.right):
        for y in range(rect.top, rect.bottom):
            (r, g, b, alpha) = image.get_at((x, y))
            if r >= exp_r and g >= exp_g and b >= exp_b:
                image.set_at((x, y), (255, 255, 255, 0))

