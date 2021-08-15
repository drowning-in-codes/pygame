import sys
import pygame
from settings import Settings
from Ship import Ship
from bullet import Bullet
from Alien import Alien
from time import sleep
from Game_stats import GameStats


class AlienInvasions:
    ''''管理游戏资源和行为的类'''

    def __init__(self):
        '''初始化游戏并创建游戏资源'''
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption(self.settings.title)
        # pygame.display.set_caption("Alien Invasion")
        # 设置背景色
        # self.bg_color = (230, 230, 230)  # rgb三元组
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        '''开始游戏的主循环'''
        while True:
            # 监视键盘和鼠标事件
            self._check_events()
            # 更新屏幕
            if self.stats.game_active:
                self.ship.update()
                # self.bullets.update()
                self._updata_bullets()
                self._update_screen()
                self._update_aliens()
                # for bullet in self.bullets.copy():
                #     if bullet.rect.bottom <= 0:
                #         self.bullets.remove(bullet)

    def _check_keydown_events(self, event):
        '''响应按键'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''相应松开'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _updata_bullets(self):
        '''更新子弹位置并删除消失子弹'''
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_events(self):
        '''响应鼠标和键盘事件'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_RIGHT:
                # 向右移动飞船
                #  self.ship.rect.x += 10
                #      self.ship.moving_right = True
                #  # if event.type == pygame.K_LEFT:
                #  #     self.ship.rect.x -=10
                #  if event.key == pygame.K_LEFT:
                #      self.ship.moving_left = True
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                # if event.key == pygame.K_RIGHT:
                #     self.ship.moving_right = False
                # if event.key == pygame.K_LEFT:
                #     self.ship.moving_left = False
                self._check_keyup_events(event)

    def _update_screen(self):
        # self.screen.fill(self.settings.bg_color)
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _fire_bullet(self):
        '''创建一颗子弹 将其加入编组中'''
        # 限制数量 当子弹数量小于限制数量时
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        '''创建外星人群'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_hight = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_hight)
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # 创建一个外星人
        alien = Alien(self)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        '''更新外星人群中所有外星人的位置'''
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''将整群外星人下移动  并换左右方向'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        '''相应子弹和外星人碰撞'''
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # 删除现有的所有子弹 并创建外星人
            self.bullets.empty()
            self._create_fleet()

    def _ship_hit(self):
        '''响应飞船被外星人碰撞'''
        # 将left-1
        if self.stats.ships_left>0:
            self.stats.ships_left -= 1
            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            # 创建一群新的外星人 并将飞船放到屏幕的底端
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        # 检查外星人是否到达底端
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break


if __name__ == '__main__':
    # 创建游戏实例并运行
    ai = AlienInvasions()
    ai.run_game()
