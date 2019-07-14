# 网页选择器
from bs4 import BeautifulSoup
import requests
import json

'''
思路：
1.使用网络请求包去请求网站 利用这个包去获取这个网站的前端源代码 这个包拿的数据是html源代码
2.在前端源代码中筛选出我们想要的数据 数据筛选用 bs4
3.把筛选出来的数据放到文件中 
'''

# 模拟浏览器
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

# 去获取请求页面 url 等下要做实例化给他一个值
def getPage(url):
    try:
        response = requests.get(url, headers=headers)
        # 在http请求状态码：200->OK； 400->请求错误；404->网页没找到；500->服务器宕机
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception:
        return None

# 获取电影信息
def getInfo(html):
    # 使用BeautifulSoup匹配电影的排行 海报 电影名 主演 评分
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('dd') #找到网页里的所有dd标签
    # 从dd标签中提取排行 海报 电影名 主演 评分
    for item in items:
        index = item.find(name='i', class_='board-index').get_text()
        name  = item.find(name='p', class_='name').get_text()
        stars = item.find(name='p', class_='star').get_text().strip()[3:]
        time  = item.find(name='p', class_='releasetime').get_text()[5:]
        score = item.find(name='p', class_='score').get_text()

        # 生成器 充当return使用 yield方法在生成对象的时候有惰性机制
        #   当被调用的时候才会返回数据，节约系统内存 
        yield {
            '排行': index, 
            '电影名称': name,
            '主演': stars,
            '上映时间': time,
            '评分': score
        }

def writeData(field):
    # 文件处理
    with open('猫眼电影排行.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(field, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    for num in [i*10 for i in range(0, 11)]:
        url = 'https://maoyan.com/board/4?offset=' + str(num)
        html = getPage(url)

        for item in getInfo(html):
            print(item)
            writeData(item)
        


