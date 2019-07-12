#我的第一个python程序
'''
def hello():
    print("HelloWorld!")
    print("Welcome to Zhangchen's Python.")

if __name__ == '__main__':
	hello()
'''

import requests
from lxml import etree
import os

class Spider(object):
    def index_request(self):
        # 1.请求首页拿到HTML数据，抽取小说名/链接 创建文件夹
        response = requests.get("https://www.qidian.com/all")
        html = etree.HTML(response.text) #整理成文档对象
        Bigtitle_list = html.xpath('//div[@class="book-mid-info"]/h4/a/text()')
        Bigsrc_list = html.xpath('//div[@class="book-mid-info"]/h4/a/@href')
        for Bigtitle, Bigsrc in zip(Bigtitle_list, Bigsrc_list):
            print(Bigtitle, Bigsrc)
            if os.path.exists(Bigtitle) == False:
                os.mkdir(Bigtitle)
            self.detail_request(Bigtitle, Bigsrc)
    
    def detail_request(self, Bigtitle, Bigsrc):
        # 2.请求目录拿到HTML数据，抽取章节名/链接
        response = requests.get("https:" + Bigsrc)
        html = etree.HTML(response.text) #整理成文档对象
        Smalltitle_list = html.xpath('//ul[@class="cf"]/li/a/text()')
        Smallsrc_list = html.xpath('//ul[@class="cf"]/li/a/@href')
        for Smalltitle, Smallsrc in zip(Smalltitle_list, Smallsrc_list):
            self.content_request(Bigtitle, Smalltitle, Smallsrc)

    def content_request(self, Bigtitle, Smalltitle, Smallsrc):
        # 3.请求文章拿到HTML数据，抽取文章内容，保存文章数据
        response =  requests.get("https:" + Smallsrc)
        html = etree.HTML(response.text) #整理成文档对象
        content = "\n".join(html.xpath('//div[@class="read-content j_readContent"]/p/text()'))

        fileName =  Bigtitle + "\\" + Smalltitle + ".txt"
        print("正在保存小说文件：" + fileName)
        with open(fileName, "w", encoding="utf-8") as f:
            f.write(content)

#执行爬虫
spider = Spider()
spider.index_request()


