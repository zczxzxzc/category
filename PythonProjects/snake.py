import os
import random
import sys
import pygame
from pygame.locals import *

# 1/定义颜色变量
# 饵食为红色 背景为黑色 贪吃🐍身体为白色
RED_COLOR = pygame.Color(255, 0, 0)
BLACK_COLOR = pygame.Color(0, 0, 0)
WHITE_COLOR = pygame.Color(255, 255, 255)
TEXT_COLOR = (60, 200, 180)
TEXT_FONT = 'microsoftyaheimicrosoftyaheiui'

class GameEnv(object):
    def __init__(self):
        pygame.init()
        # 创建显示层(游戏界面)
        pygame.display.set_caption('贪吃蛇')
        self.play_surface = pygame.display.set_mode((800, 600), flags=SRCALPHA, depth=32)
        pygame.event.set_blocked(MOUSEMOTION)
        pygame.mixer.init()

class Snake(object):
    def __init__(self):
        self.game_env = GameEnv()
        self.username = ''
        self.is_gameover = False
        self.speed = 100
        # 初始化🐍的起始坐标和长度(列表长度表示身体长度)
        self.head = [(random.randint(1, 20))*20, (random.randint(1, 29))*20]
        self.body = []
        for i in range(132):
            self.body.append([self.head[0]-2*i, self.head[1]])
        # 定义目标方块
        self.gen_target()
        self.score = 0
        # 初始化目标方向右
        self.direction = 'right'
        self.change_direction = self.direction
        # 初始化图像信息
        self.init_image()


    def init_image(self):
        self.head_image_right = pygame.image.load(os.path.join('img', 'sneak_head_right.png')).convert_alpha()
        self.head_image_left = pygame.image.load(os.path.join('img', 'sneak_head_left.png')).convert_alpha()
        self.head_image_up = pygame.image.load(os.path.join('img', 'sneak_head_up.png')).convert_alpha()
        self.head_image_down = pygame.image.load(os.path.join('img', 'sneak_head_down.png')).convert_alpha()
        self.head_image_right.set_alpha(255)
        self.head_image_left.set_alpha(255)
        self.head_image_up.set_alpha(255)
        self.head_image_down.set_alpha(255)

        self.body_image_horizontal = pygame.image.load(os.path.join('img', 'sneak_body_horizontal.png')).convert_alpha()
        self.body_image_vertical = pygame.image.load(os.path.join('img', 'sneak_body_vertical.png')).convert_alpha()
        self.body_image_left_down = pygame.image.load(os.path.join('img', 'sneak_body_left_down.png')).convert_alpha()
        self.body_image_left_up = pygame.image.load(os.path.join('img', 'sneak_body_left_up.png')).convert_alpha()
        self.body_image_right_down = pygame.image.load(os.path.join('img', 'sneak_body_right_down.png')).convert_alpha()
        self.body_image_right_up = pygame.image.load(os.path.join('img', 'sneak_body_right_up.png')).convert_alpha()
        self.body_image_horizontal.set_alpha(255)
        self.body_image_vertical.set_alpha(255)
        self.body_image_left_down.set_alpha(255)
        self.body_image_left_up.set_alpha(255)
        self.body_image_right_down.set_alpha(255)
        self.body_image_right_up.set_alpha(255)

        self.tail_image_right = pygame.image.load(os.path.join('img', 'sneak_tail_right.png')).convert_alpha()
        self.tail_image_left = pygame.image.load(os.path.join('img', 'sneak_tail_left.png')).convert_alpha()
        self.tail_image_up = pygame.image.load(os.path.join('img', 'sneak_tail_up.png')).convert_alpha()
        self.tail_image_down = pygame.image.load(os.path.join('img', 'sneak_tail_down.png')).convert_alpha()
        self.target_image = pygame.image.load(os.path.join('img', 'chicken.png')).convert_alpha()
        self.tail_image_right.set_alpha(255)
        self.tail_image_left.set_alpha(255)
        self.tail_image_up.set_alpha(255)
        self.tail_image_down.set_alpha(255)
        self.target_image.set_alpha(255)

        self.background_image = pygame.image.load(os.path.join('img', 'background.png')).convert()


    def welcome(self):
        screen = self.game_env.play_surface
        username = []
        pygame.mixer.music.load(os.path.join('music', 'warmup.mp3'))
        pygame.mixer.music.play()
        while True:
            for event in pygame.event.get():  # 从队列中获取事件
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE and len(username)>0:
                        username = username[0:-1]
                    elif event.key == K_RETURN and len(username)>0:
                        pygame.mixer.music.fadeout(200)
                        return
                    elif event.key == K_MINUS  and len(username)<15:
                        username.append("_")
                    elif event.key <= 127 and len(username)<15:
                        if event.mod in [KMOD_LSHIFT, KMOD_RSHIFT, KMOD_SHIFT, KMOD_CAPS]:
                            username.append(chr(event.key).upper())
                        else:
                            username.append(chr(event.key))
            self.username = ''.join(username)
            screen.blit(self.background_image,[0 ,0 ,800, 600])
            text1 = "WELCOME"
            text2 = "Pleas input your name:"
            text3 = self.username
            ft1_font = pygame.font.SysFont(TEXT_FONT, 50)
            ft1_surf = ft1_font.render( text1, 1, TEXT_COLOR)
            ft2_font = pygame.font.SysFont(TEXT_FONT, 40)
            ft2_surf = ft2_font.render( text2, 1, TEXT_COLOR)
            ft3_font = pygame.font.SysFont(TEXT_FONT, 40)
            ft3_surf = ft3_font.render( text3, 1, TEXT_COLOR)
            screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 50])
            screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 120])
            screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 200])
            pygame.display.flip()

    def pause(self):
        screen = self.game_env.play_surface
        self.draw()
        pause_text1 = "GAME PAUSED"
        pause_text2 = "Your current score is:  " + str(self.score)
        pause_text3 = "Press any key to continue"
        ft1_font = pygame.font.SysFont(TEXT_FONT, 50)
        ft1_surf = ft1_font.render( pause_text1, 1, TEXT_COLOR)
        ft2_font = pygame.font.SysFont(TEXT_FONT, 40)
        ft2_surf = ft2_font.render( pause_text2, 1, TEXT_COLOR)
        ft3_font = pygame.font.SysFont(TEXT_FONT, 40)
        ft3_surf = ft3_font.render( pause_text3, 1, TEXT_COLOR)
        screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 50])
        screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 120])
        screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 200])
        # TODO 显示排行榜
        pygame.display.flip()

        pygame.time.delay(200)
        pygame.event.clear()
        while True:
            if pygame.mixer.music.get_busy()==False:
                pygame.mixer.music.load(os.path.join('music', 'BGM'+ str(random.randint(1, 2)) +'.mp3'))
                pygame.mixer.music.play()
            for event in pygame.event.get():  # 从队列中获取事件
                if event.type == KEYDOWN:
                    return

    def game_over(self):
        pygame.time.delay(200)
        screen = self.game_env.play_surface
        self.draw()
        final_text1 = "GAME OVER"
        final_text2 = "Your final score is:  " + str(self.score)
        final_text3 = "Press 'ESC' to quit,'r' to restart."
        # 设置第一行文字字体
        ft1_font = pygame.font.SysFont(TEXT_FONT, 50)
        ft1_surf = ft1_font.render( final_text1, 1, TEXT_COLOR)
        ft2_font = pygame.font.SysFont(TEXT_FONT, 40)
        ft2_surf = ft2_font.render( final_text2, 1, TEXT_COLOR)
        ft3_font = pygame.font.SysFont(TEXT_FONT, 40)
        ft3_surf = ft3_font.render( final_text3, 1, TEXT_COLOR)
        screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 50])
        screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 120])
        screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 200])
        # TODO 计算并显示排行榜
        pygame.display.flip()
        self.is_gameover = True
        pygame.mixer.music.fadeout(500)
        pygame.mixer.music.queue(os.path.join('music', 'rest.mp3'))
        pygame.time.delay(1000)
        pygame.event.clear()
        return

    def isCrashed(self):
        # 撞墙判定
        if (self.head[0] > 780) or (self.head[0] < 0) or (self.head[1] > 580) or (self.head[1] < 0):
            return True
        # 身体碰撞判定
        for body in self.body:
            if (self.direction == 'up' and body[0] == self.head[0] and (body[1] < self.head[1] and body[1]+20 >= self.head[1]))\
                    or(self.direction == 'down'and body[0] == self.head[0] and (body[1] > self.head[1] and body[1] <= self.head[1]+20))\
                    or(self.direction == 'left' and (body[0] < self.head[0] and body[0]+20 >= self.head[0]) and body[1] == self.head[1])\
                    or(self.direction == 'right' and (body[0] > self.head[0] and body[0] <= self.head[0]+20) and body[1] == self.head[1]):
                return True
        return False

    def gen_target(self):
        while True:
            self.targetPosition = [
                (random.randint(1, 31))*20, (random.randint(1, 23))*20]
            if self.targetPosition not in self.body:
                break
        return

    def move(self):
        # 判断输入方向的有效性
        if (self.change_direction == 'left' and self.direction != 'right')\
                or(self.change_direction == 'right' and self.direction != 'left')\
            or(self.change_direction == 'up' and self.direction != 'down')\
                or(self.change_direction == 'down' and self.direction != 'up'):
            self.direction = self.change_direction
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
            self.gen_target()
            self.score += 10
            # 控制速度,每吃掉2个饵速度就加一点
            if (self.score % 20 == 0):
                self.speed += 10
            # 增长一节
            x = self.body[-1][0]-self.body[-2][0]
            y = self.body[-1][1]-self.body[-2][1]
            for _ in range(10):
                newtail = [self.body[-1][0]+x, self.body[-1][1]+y]
                self.body.append(newtail)
        return True

    def run(self, speed):
        pygame.event.set_allowed([KEYDOWN, QUIT])
        i = 0
        self.speed = speed
        self.welcome()
        while True:
            if self.is_gameover == False:
                #如果没有音乐流则加载播放BGM
                if pygame.mixer.music.get_busy()==False:
                    pygame.mixer.music.load(os.path.join('music', 'BGM'+ str(random.randint(1, 2)) +'.mp3'))
                    pygame.mixer.music.play()
                if i == 10:
                    i = 0
                    for event in pygame.event.get():  # 从队列中获取事件
                        if event.type == QUIT:
                            self.pause()
                            continue
                        elif event.type == KEYDOWN:
                            if event.key == K_RIGHT:
                                self.change_direction = 'right'
                            if event.key == K_LEFT:
                                self.change_direction = 'left'
                            if event.key == K_UP:
                                self.change_direction = 'up'
                            if event.key == K_DOWN:
                                self.change_direction = 'down'
                            if event.key == K_ESCAPE:
                                # pygame.event.post(pygame.event.Event(QUIT))
                                self.pause()
                    if self.move() == True:
                        self.draw()
                    else:
                        self.game_over()
                else:
                    if self.move() == True:
                        self.draw()
                    else:
                        self.game_over()
                i += 1
            else:
                #加载音乐
                if pygame.mixer.music.get_busy()==False:
                    pygame.mixer.music.load(os.path.join('music', 'rest.mp3'))
                    pygame.mixer.music.play()
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            return False
                        else:
                            return True
            # 通过fps实现速度变化
            pygame.time.Clock().tick(self.speed)


    def draw(self):
        screen = self.game_env.play_surface
        screen.blit(self.background_image,[0 ,0 ,800, 600])
        # 逐节画身体，靠后一段的相对位置判断横竖方向
        for i in range(1,len(self.body)-1)[::2]:
            if self.body[i][0] != self.body[i+1][0]:
                screen.blit(self.body_image_horizontal, [self.body[i][0], self.body[i][1], 20, 20])
            else:
                screen.blit(self.body_image_vertical, [self.body[i][0], self.body[i][1], 20, 20])
        # 转弯处需要单独描绘
        for i in range(1,len(self.body)-1):
            if self.body[i][0]*2 - self.body[i+1][0] - self.body[i-1][0] > 0:  #左边有节点
                if self.body[i][1]*2 - self.body[i+1][1] - self.body[i-1][1] > 0:
                    screen.blit(self.body_image_left_up, [self.body[i][0], self.body[i][1], 20, 20])
                elif self.body[i][1]*2 - self.body[i+1][1] - self.body[i-1][1] < 0:
                    screen.blit(self.body_image_left_down, [self.body[i][0], self.body[i][1], 20, 20])
            elif self.body[i][0]*2 - self.body[i+1][0] - self.body[i-1][0] < 0:
                if self.body[i][1]*2 - self.body[i+1][1] - self.body[i-1][1] > 0:
                    screen.blit(self.body_image_right_up, [self.body[i][0], self.body[i][1], 20, 20])
                elif self.body[i][1]*2 - self.body[i+1][1] - self.body[i-1][1] < 0:
                    screen.blit(self.body_image_right_down, [self.body[i][0], self.body[i][1], 20, 20])
        # 尾巴只能通过前方节点判断方向
        if self.body[-1][1] > self.body[-3][1]:
            screen.blit(self.tail_image_up, [self.body[-1][0], self.body[-1][1], 20, 20])
        elif self.body[-1][1] < self.body[-3][1]:
            screen.blit(self.tail_image_down, [self.body[-1][0], self.body[-1][1], 20, 20])
        elif self.body[-1][0] > self.body[-3][0]:
            screen.blit(self.tail_image_left, [self.body[-1][0], self.body[-1][1], 20, 20])
        else:
            screen.blit(self.tail_image_right, [self.body[-1][0], self.body[-1][1], 20, 20])
        # 画蛇头
        if self.direction == 'right':
            screen.blit(self.head_image_right, [self.head[0], self.head[1], 20, 20])
        if self.direction == 'left':
            screen.blit(self.head_image_left, [self.head[0], self.head[1], 20, 20])
        if self.direction == 'down':
            screen.blit(self.head_image_down, [self.head[0], self.head[1], 20, 20])
        if self.direction == 'up':
            screen.blit(self.head_image_up, [self.head[0], self.head[1], 20, 20])

        screen.blit(self.target_image, [self.targetPosition[0], self.targetPosition[1], 20, 20])
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
