import pygame
import sys
import math
from settings import Settings
# 一个frame对象由5个值组成
# 为减小启动时间, 可以事先把frame列表和四个边界值加载到json文件
class Frame():
    # 代表一个火柴人的外部框架，用以碰撞检测
    # 在火柴人的外表加一层白色的颜色层，当这一层东西颜色变了，发生了碰撞
    # get_at(pos), set_at(pos, color)表示读取与设置surface中一个像素点的颜色
    def __init__(self, image, settings, from_file = False, frame = [], frame_rect = {}):
        self.frame = []                  #表示第几行的人物外框
        if from_file == False :
            self.frame_rect = {
                "top" : 300,
                "bottom" : 0,
                "left" : 300,
                "right" : 0,
            }
            self.build_frame(image, settings.hero_boot_color)
        else :
            self.frame_rect = frame_rect
            self.frame = frame


    def build_frame(self, image, hero_boot_color):
        rect = image.get_rect()
        rect.top = 0
        rect.left = 0
        self.frame_rect["top"] = rect.bottom
        self.frame_rect["bottom"] = rect.top
        self.frame_rect["left"] = rect.right
        self.frame_rect["right"] = rect.left
        for y in range(rect.top, rect.bottom):
            left = 0
            right = 0
            x = rect.left
            while x < rect.right :
                (r, g, b, alpha) = image.get_at((x, y))
                if r < 20 and r == g and r == b:
                    left = x
                    break 
                x += 1
            x = rect.right
            while x > rect.left:
                x -= 1
                (r, g, b, alpha) = image.get_at((x, y))
                if r < 20 and r == g and r == b:
                    right = x
                    break
            if left > right:
                left = 0
                right = 0
            if left > 0 :
                left -= 1
            if right != 0 and right + 1 < rect.right :
                right += 1
            self.frame.append({"left" : [], "right" : []})             #
            if left != right:
                self.frame_rect["top"] = min (y, self.frame_rect["top"])
                self.frame_rect["bottom"] = max(y, self.frame_rect["bottom"])
                self.frame_rect["left"] = min(self.frame_rect["left"]+1, left)
                self.frame_rect["right"] = max(self.frame_rect["right"]-1, right)
                image.set_at((left, y), hero_boot_color)
                image.set_at((right, y), hero_boot_color)
                self.frame[-1]["left"].append(left)
                self.frame[-1]["right"].append(right)
                if len(self.frame) > 1 and len(self.frame[-2]["left"]) > 0 :
                    last = self.frame[-2]["left"][0]
                    this = self.frame[-1]["left"][0]
                    while this != last :
                        #当上下行的外框点不连通时, 连一条线
                        if last > this :
                            last -= 1
                            self.frame[-2]["left"].append(last)
                            image.set_at((last, y-1), hero_boot_color)
                        else :
                            this -= 1
                            self.frame[-1]["left"].append(this)
                            image.set_at((this, y), hero_boot_color)
                if len(self.frame) > 1 and len(self.frame[-2]["right"]) > 0 :
                    last = self.frame[-2]["right"][0]
                    this = self.frame[-1]["right"][0]
                    while this != last :
                        #当上下行的外框点不连通时, 连一条线
                        if last < this :
                            last += 1
                            self.frame[-2]["right"].append(last)
                            image.set_at((last, y-1), hero_boot_color)
                        else :
                            this += 1
                            self.frame[-1]["right"].append(this)
                            image.set_at((this, y), hero_boot_color)