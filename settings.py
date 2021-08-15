class Settings:
    '''存储游戏中所设置的类'''
    def __init__(self):
        '''初始化游戏的设置'''
        # 屏幕的设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.title = "Alien Invasion"
        # 飞船的速度
        self.ship_speed = 1.5  #每次移动1.5个像素
        # 子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3
        self.alien_speed = 1.0
        self.fleet_drop_speed = 8.0  #当外星人撞到屏幕边缘时 外星人群向下移动的速度
        #1为右移 -1为左移
        self.fleet_direction = 1
        #船的数量
        self.ship_limit = 3