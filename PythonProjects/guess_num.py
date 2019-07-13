
import random

def produceNumInRange(minValue, maxVlaue):
    return random.randint(minValue, maxVlaue)

def getinput():
    print('请输入最小值：')
    minVlaue = int(input())
    print('请输入最大值：')
    maxVlaue = int(input())
    return minVlaue, maxVlaue

def hello():
    minVlaue, maxVlaue = getinput()
    print('正在生成随机数值……')
    produceNumInRange(minVlaue, maxVlaue)
    print('完成！\n请输入猜拳数值：')
