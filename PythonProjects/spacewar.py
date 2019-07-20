# 调用pygame模块
import pygame
# 调用random模块
import random
# 调用 pygame.locals 使容易使用关键参数
from pygame.locals import *
# 定义Player对象 调用super赋予它属性和方法
# 我们画在屏幕上的surface 现在是player的一个属性


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_key):
        if pressed_key == K_UP:
            self.rect.move_ip(0, -5)
        if pressed_key == K_DOWN:
            self.rect.move_ip(0, 5)
        if pressed_key == K_LEFT:
            self.rect.move_ip(-5, 0)
        if pressed_key == K_RIGHT:
            self.rect.move_ip(5, 0)
        # 限定player在屏幕中
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(820, random.randint(0, 600)))
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# 初始化 pygame
pygame.init()
# 创建屏幕对象
# 设定尺寸为 800x600
screen = pygame.display.set_mode((800, 600))
# 为添加敌人创建自定义事件
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
# 初始化Player， 现在他仅仅是一个矩形
player = Player()
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
# 控制主循环的进行的变量
running = True
# 主循环
while running:
    # 事件队列中的循环
    for event in pygame.event.get():
        # 检测 KEYDOWN: KEYDOWN 是我们定义好的pygame.locals中的一个常量
        if event.type == KEYDOWN:
            # 按下 Esc 键则退出主程序
            if event.key == K_ESCAPE:
                running = False
            # 检测 QUIT 到则终止
            player.update(event.key)
        elif event.type == QUIT:
            running = False
        elif(event.type == ADDENEMY):
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    # 这一行表示：将surf画到屏幕 x：400.y:300的坐标上
    screen.blit(player.surf, (400, 300))
    # 更新
    pygame.display.flip()
