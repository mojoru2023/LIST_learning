# 写个小脚本就搞定了！
import re

import pymysql

import time

import requests
from requests.exceptions import ConnectionError
from selenium import webdriver
from lxml import etree
import datetime
# driver = webdriver.Firefox()
from requests.exceptions import RequestException

#请求  关键在于遍历点击 (操作动作细分！)
# 1. 登录页面可以复用
#2. 点击个人页面，寻求遍历
#3. 点击个人页面，然后翻页，在这个页面最终关闭浏览器！
# 问题，遍历之后如果从最开始又回到之前的下一个！除非使用减去一个容器里面的数字，下一次绝对是最新的！

def queue_num():

    from queue import Queue
    q = Queue()
    for num in range(1, 526):
        q.put(num)
        yield q.get()

def get_one_page(url):
    headers = {"user-agent":'my-app/0.0.1'}
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None




def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    selector = etree.HTML(html)
    link = selector.xpath('//*[@id="blog"]/section/div/h2/a/@href')
    title = selector.xpath('//*[@id="blog"]/section/div/h2/a/text()')
    for i1,i2 in zip(link,title):
        yield ('https://segmentfault.com'+str(i1),i2)






#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into segmentfalut_python_blog (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass





if __name__ == '__main__':
    for offset in range(7,312):
        url = 'https://segmentfault.com/t/flask/blogs?page=' + str(offset)
        html = get_one_page(url)
        content = parse_html(html)
        insertDB(content)
        print(url)


# create table segmentfalut_python_blog(
# id int not null primary key auto_increment,
# link varchar(100),
# title varchar(100)
# ) engine=InnoDB  charset=utf8;
