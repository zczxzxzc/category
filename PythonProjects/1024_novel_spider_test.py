#我的第一个python程序
'''
def hello():
    print("HelloWorld!")
    print("Welcome to Zhangchen's Python.")

if __name__ == '__main__':
	hello()
'''

import requests_html
import os

class Spider(object):
    def index_request(self):
        session = requests_html.HTMLSession()
        r = session.get('https://cl.cfbf.xyz/thread0806.php?fid=20&search=&page=3')
        novel_list = r.html.find('#ajaxtable > tbody:nth-child(2) > tr > td.tal > h3')
        novel_list = novel_list[5:-1]
        for x in novel_list:
            title = x.text
            for reallink in x.links:
                url = 'https://cl.cfbf.xyz/' + reallink
            self.content_request(title, url)

    def content_request(self, title, url):
        session = requests_html.HTMLSession()
        r = session.get(url)

        content = r.html.find('#main > div:nth-child(4)')
        
        content = 'url:' + url + '\n' + content[0].text
        fileName = 'D:/cl/' + title + ".txt"

        print("正在保存小说文件：" + fileName)
        with open(fileName, "w", encoding="utf-8") as f:
            f.write(content)

#执行爬虫
spider = Spider()
spider.index_request()
print('the end')
