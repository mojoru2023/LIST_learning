
# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql

import time
from requests.exceptions import ConnectionError
from selenium import webdriver
from lxml import etree
import datetime

driver = webdriver.Chrome()


# 请求

def get_first_page(url):
    # driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    driver.set_window_size(1200, 1200)  # 设置窗口大小
    driver.get(url)
    html = driver.page_source
    time.sleep(6)
    return html


# 把首页和翻页处理？
#　翻页有两个解决办法：
# 1. 倒叙遍历列表
# 2.点击下一页操作！
# 这个地方倾向于倒序遍历






def parse_html(html):  # 正则专门有反爬虫的布局设置，不适合爬取表格化数据！
    big_list = []
    selector = etree.HTML(html)
    title = selector.xpath('//*[@id="common-packages"]//div[1]/h4/text()')
    content = selector.xpath('//*[@id="common-packages"]//div[2]/p/text()')
    link = selector.xpath('//*[@id="common-packages"]/a/@href')
    for i1, i2,i3 in zip(title, content,link):
        link_f = "https://www.bootcdn.cn"+i3
        big_list.append((i1,i2,link_f))


    return big_list







# 存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into BootCDN (title,content,link) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration:
        pass


if __name__ == '__main__':
    url = 'https://www.bootcdn.cn/all/'
    html = get_first_page(url)
    content = parse_html(html)
    insertDB(content)




# 字段设置了唯一性 unique

# create table BootCDN(
# id int not null primary key auto_increment,
# title text,
# content text,
# link varchar(100)
# ) engine=InnoDB  charset=utf8;

# 传入url太快了，考虑分成两部分完成：1.先存到数据库中或其他容器中（数据结构不行）
#  2. 再从数据库中逐个调取进行爬取   3. 中间过渡的数据库是用内存型（redis) 还是一般存储型的？
# 4.数据量小，爬取，传入，再解析影响不大，但是分布式爬取大量数据，就必须要切割开来，才能各司其职，有效处理各自的工作！
# 5.容器是必备，分布式必备，代理池也是必备

