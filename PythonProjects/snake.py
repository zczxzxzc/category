
import random
import sys
import pygame
from pygame.locals import *

# 1/定义颜色变量
# 饵食为红色 背景为黑色 贪吃🐍身体为白色
redColor    = pygame.Color(255,0,0)
blackColor  = pygame.Color(0,0,0)
whiteColor  = pygame.Color(255,255,255)

class GameEnv(object):
    def __init__(self):
        pygame.init()
        # 创建显示层(游戏界面)
        pygame.display.set_caption('贪吃蛇')
        self.playSurface = pygame.display.set_mode((800, 600))

class Snake(object):
    def __init__(self):
        self.gameEnv = GameEnv()
        self.isGameover = False
        self.speed = 100
        # 初始化🐍的起始坐标和长度(列表长度表示身体长度)
        self.head = [(random.randint(1, 20))*20, (random.randint(1, 29))*20]
        self.body = []
        for i in range(120):
            self.body.append([self.head[0]-2*i, self.head[1]])
        # 定义目标方块
        self.genTarget()
        self.score = 0
        # 初始化目标方向右
        self.direction = 'right'
        self.changeDirection = self.direction

    def gameOver(self):
        # 显示分数
        screen = self.gameEnv.playSurface
        final_text1 = "Game Over"
        final_text2 = "Your final score is:  " + str(self.score)
        final_text3 = "Press any key to restart"
        ft1_font = pygame.font.SysFont("Arial", 70)                                      # 设置第一行文字字体
        ft1_surf = ft1_font.render(final_text1, 1, (242, 3, 36))                         # 设置第一行文字颜色
        ft2_font = pygame.font.SysFont("Arial", 50)                                      # 设置第二行文字字体
        ft2_surf = ft2_font.render(final_text2, 1, (253, 177, 6))                        # 设置第二行文字颜色
        ft3_font = pygame.font.SysFont("Arial", 50)                                      # 设置第三行文字字体
        ft3_surf = ft3_font.render(final_text3, 1, (180, 180, 0))                        # 设置第三行文字颜色
        screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 150])  # 设置第一行文字显示位置
        screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 300])  # 设置第二行文字显示位置
        screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 450])  # 设置第三行文字显示位置
        pygame.display.flip()
        pygame.display.update()    # 更新显示
        self.isGameover = True
        pygame.event.clear()
        return

    def isCrashed(self):
        # 撞墙判定
        if (self.head[0] > 780) or (self.head[0] < 0) or (self.head[1] > 580) or (self.head[1] < 0):
            return True
        # 身体碰撞判定
        for body in self.body:
            if (self.direction == 'up' and body[0]==self.head[0] and ( body[1] < self.head[1] and body[1]+20 >= self.head[1] ))\
                or(self.direction == 'down'and body[0]==self.head[0] and (body[1] > self.head[1] and body[1] <= self.head[1]+20))\
                or(self.direction == 'left' and ( body[0] < self.head[0] and body[0]+20 >= self.head[0] ) and body[1]==self.head[1])\
                or(self.direction == 'right' and ( body[0] > self.head[0] and body[0] <= self.head[0]+20 ) and body[1]==self.head[1]):
                return True
        return False

    def genTarget(self):
        while True:
            self.targetPosition = [(random.randint(1, 31))*20, (random.randint(1, 23))*20]
            if self.targetPosition not in self.body :
                break
        return

    def move(self):
        # 判断输入方向的有效性
        if (self.changeDirection == 'left' and not self.direction == 'right')\
            or(self.changeDirection == 'right' and not self.direction == 'left')\
                or(self.changeDirection == 'up' and not self.direction == 'down')\
                    or(self.changeDirection == 'down' and not self.direction == 'up'):
                    self.direction = self.changeDirection
        # 根据方向移动蛇头
        if self.direction == 'right':
            self.head[0] += 2
        if self.direction == 'left':
            self.head[0] -= 2
        if self.direction == 'down':
            self.head[1] += 2
        if self.direction == 'up':
            self.head[1] -= 2
        # 碰撞则游戏结束
        if self.isCrashed():
            return False

        for i in range(len(self.body)-1):
            self.body[len(self.body)-i-1] = list(self.body[len(self.body)-i-2])
        self.body[0] = list(self.head)
        if self.head[0] == self.targetPosition[0] and self.head[1] == self.targetPosition[1]:
            self.genTarget()
            self.score += 10
            # 控制速度,每吃掉5个饵速度就加一点
            if (self.score % 50 == 0):
                self.speed += 3
            # 增长一节
            x = self.body[-1][0]-self.body[-2][0]
            y = self.body[-1][1]-self.body[-2][1]
            for i in range(10):
                newtail = [self.body[-1][0]+x, self.body[-1][1]+y]
                self.body.append(newtail)
        return True

    def run(self, speed):
        i = 0
        self.speed = speed
        while True:
            if self.isGameover == False:
                if i == 10:
                    i = 0
                    for event in pygame.event.get(): # 从队列中获取事件
                        if event.type == QUIT:
                            self.gameOver()
                            break
                        elif event.type == KEYDOWN:
                            if event.key == K_RIGHT:
                                self.changeDirection = 'right'
                            if event.key == K_LEFT:
                                self.changeDirection = 'left'
                            if event.key == K_UP:
                                self.changeDirection = 'up'
                            if event.key == K_DOWN:
                                self.changeDirection = 'down'
                            if event.key == K_ESCAPE:
                                pygame.event.post(pygame.event.Event(QUIT))
                    if self.move() == True:
                        self.draw()
                    else:
                        # TODO: 怎样实现继续循环等待，在捕获按键动作时再return True？
                        self.gameOver()
                        continue
                else:
                    if self.move() == False:
                        self.gameOver()
                    else:
                        self.draw()
                i += 1
            # TODO: 怎样实现继续循环等待，在捕获按键动作时再return True？
            else:
                for event in pygame.event.get(): # 从队列中获取事件
                    if event.type == QUIT:
                        return False
                    elif event.type == KEYDOWN:
                        return True
            fps = pygame.time.Clock()
            fps.tick(self.speed)

    def draw(self):
        surface = self.gameEnv.playSurface
        surface.fill(blackColor)
        for position in self.body:
            pygame.draw.rect(surface, whiteColor, Rect(position[0], position[1], 20, 20))
            pygame.draw.rect(surface, redColor, Rect(self.targetPosition[0], self.targetPosition[1], 20, 20))
        pygame.display.flip()

if __name__ == '__main__':
    snake = Snake()
    while True:
        if snake.run(100) == False:
            break
        snake.__init__()
    pygame.quit()
    sys.exit()
    print('end')