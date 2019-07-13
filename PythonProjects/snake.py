
import random, sys, pygame, copy
from pygame.locals import *

# 1/定义颜色变量
# 饵食为红色 背景为黑色 贪吃🐍身体为白色
redColor    = pygame.Color(255,0,0)
blackColor  = pygame.Color(0,0,0)
whiteColor  = pygame.Color(255,255,255)

# 2/定义游戏结束的函数


class GameEnv(object):
    def __init__(self):
        pygame.init()
        # 创建显示层(游戏界面)
        pygame.display.set_caption('贪吃蛇')
        self.playSurface = pygame.display.set_mode((640, 480))

class Snake(object):
    def __init__(self, ):
        self.gameEnv = GameEnv()
        # 初始化🐍的起始坐标和长度(列表长度表示身体长度)
        self.head = [(random.randint(1, 15))*20, (random.randint(1, 22))*20]
        self.body = [[0,0],[0,0],[0,0]]
        for i in range(3):
            self.body[i][0] = self.head[0]-20*i
            self.body[i][1] = self.head[1]
        # 定义目标方块
        self.genTarget()
        self.score = 0
        # 初始化目标方向右
        self.direction = 'right'
        self.changeDirection = self.direction

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
            self.head[0] += 20
        if self.direction == 'left':
            self.head[0] -= 20
        if self.direction == 'down':
            self.head[1] += 20
        if self.direction == 'up':
            self.head[1] -= 20
        # 撞墙则游戏结束 TODO
        if self.head[0] > 620 or self.head[0] < 0:
            self.gameOver()
            return False
        elif self.head[1] > 460 or  self.head[1] < 0:
            self.gameOver()
            return False

        self.body.insert(0, list(self.head))
        if self.head[0] == self.targetPosition[0] and self.head[1] == self.targetPosition[1]:
            self.genTarget()
            self.score += 10
        else:
            self.body.pop()
        return True

    def run(self, speed):
        while True:
            for event in pygame.event.get(): # 从队列中获取事件
                if event.type == QUIT:
                    self.gameOver()
                    return False
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
                # TODO 怎样实现按键继续？
                return
                    # 控制速度
            fps = pygame.time.Clock()
            fps.tick(speed)

    def draw(self):
        surface = self.gameEnv.playSurface
        surface.fill(blackColor)
        for position in self.body:
            pygame.draw.rect(surface, whiteColor, Rect(position[0], position[1], 20, 20))
            pygame.draw.rect(surface, redColor, Rect(self.targetPosition[0], self.targetPosition[1], 20, 20))
        pygame.display.flip()

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
        screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
        screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 250])  # 设置第二行文字显示位置
        # screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 350])  # 设置第三行文字显示位置
        pygame.display.flip()
        pygame.display.update()    # 更新显示
        
        return

if __name__ == '__main__':
    snake = Snake()
    while True:
        snake.__init__()
        snake.run(5)
    sys.exit()
    pygame.quit()
