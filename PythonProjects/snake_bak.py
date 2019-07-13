
import random, sys, pygame
from pygame.locals import *

# 1/定义颜色变量
# 饵食为红色 背景为黑色 贪吃🐍身体为白色
redColor    = pygame.Color(255,0,0)
blackColor  = pygame.Color(0,0,0)
whiteColor  = pygame.Color(255,255,255)

# 2/定义游戏结束的函数
def gameOver(Score):
    pygame.quit()
    sys.exit()

class Snake(object):
    def __init__(self):
        self.head = [(random.randint(1, 15))*20, (random.randint(1, 22))*20]
        self.body = [[0,0],[0,0],[0,0]]
        for i in range(3):
            self.body[i][0] = self.head[0]-20*i
            self.body[i][1] = self.head[1]
        while True:
            self.targetPosition = [(random.randint(1, 15))*20, (random.randint(1, 22))*20]
            if self.targetPosition not in self.body :
                break
        self.targetFlag = 1
        self.score = 0
        self.direction = 'right'
        self.changeDirection = self.direction
    def move(self, direction):
        return


class GameEnv(object):
    def __init__(self, speed):
        pygame.init()
        pygame.display.set_caption('贪吃蛇')
        self.playSurface = pygame.display.set_mode((640, 480))
        self.fps = pygame.time.Clock()
        self.fps.tick(speed)


# 3/定义main函数
def example():
    pygame.init()
    # 控制速度
    fpsClock = pygame.time.Clock()
    # 创建显示层(游戏界面)
    playSurface = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('贪吃蛇')
    # 初始化🐍的起始坐标和长度(列表长度表示身体长度)
    SnakePosition = [100, 100]
    snakeBody = [[100, 100], [80, 100], [60, 100]]
    # 定义目标方块 flag标记是否已吃掉目标(1：没有，0：吃掉了)
    targetPosition = [300, 300]
    targetFlag = 1
    # 初始化目标方向右
    direction = 'right'
    changeDirection = direction
    Score = 0
    while True:
        for event in pygame.event.get(): # 从队列中获取事件
            if event.type == QUIT:
                gameOver()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    changeDirection = 'right'
                if event.key == K_LEFT:
                    changeDirection = 'left'
                if event.key == K_UP:
                    changeDirection = 'up'
                if event.key == K_DOWN:
                    changeDirection = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
        if changeDirection == 'left' and not direction == 'right': # TODO
            direction = changeDirection
        if changeDirection == 'right' and not direction == 'left':
            direction = changeDirection
        if changeDirection == 'up' and not direction == 'down':
            direction = changeDirection
        if changeDirection == 'down' and not direction == 'up':
            direction = changeDirection
        # 根据方向移动蛇头
        if direction == 'right':
            SnakePosition[0] += 20
        if direction == 'left':
            SnakePosition[0] -= 20
        if direction == 'down':
            SnakePosition[1] += 20
        if direction == 'up':
            SnakePosition[1] -= 20

        if SnakePosition[0] > 620 or SnakePosition[0] < 0:
            gameOver()
        elif SnakePosition[1] > 460 or  SnakePosition[1] < 0:
            gameOver

        snakeBody.insert(0, list(SnakePosition)) # TODO
        if SnakePosition[0] == targetPosition[0] and SnakePosition[1] == targetPosition[1]:
            targetFlag = 0
        else:
            snakeBody.pop()
        
        if targetFlag == 0: #TODO
            x = random.randrange(1, 32)
            y = random.randrange(1, 24)
            targetPosition = [int(x*20), int(y*20)]
            targetFlag = 1
        # 填充背景颜色
        playSurface.fill(blackColor)
        for position in snakeBody:
            pygame.draw.rect(playSurface, whiteColor, Rect(position[0], position[1], 20, 20))
            pygame.draw.rect(playSurface, redColor, Rect(targetPosition[0], targetPosition[1], 20, 20))
        pygame.display.flip()



        fpsClock.tick(5)

if __name__ == '__main__':
    snake = Snake()
    gameEnv = GameEnv(5)
    a = 1