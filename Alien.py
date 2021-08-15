import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''表示单个外星人'''

    def __init__(self, ai_game):
        '''初始化外星人'''
        super().__init__()
        self.screen = ai_game.screen
        # 加载外星人图像并设置大小位置
        self.image = pygame.image.load('./images/ufo.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人都从左上角产生出
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.settings = ai_game.settings
        self.x = float(self.rect.x)

    def update(self):
        '''向右移动外星人'''
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        '''如果外星人在边缘返回true'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
