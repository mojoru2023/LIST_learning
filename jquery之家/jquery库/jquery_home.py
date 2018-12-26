#! -*- coding:utf-8 -*-
import re

import requests
from lxml import etree
from selenium import webdriver
import pymysql
import datetime
import time
from requests.exceptions import RequestException

driver = webdriver.Chrome()


# 故意拼接出错误的url,减少正确解决复杂问题的难度
#　这里可以用到两个url嵌套组合！



def get_one_page(url):
    driver.get(url)
    html = driver.page_source
    return html





def parse_page(html):
    big_list = []
    selector = etree.HTML(html)
    title = selector.xpath("/html/body/div/div[2]/div//div[2]/div[1]/a/b/text()")
    link =  selector.xpath("/html/body/div/div[2]/div//div[2]/div[1]/a/@href")
    for i1,i2 in zip(title,link):
        big_list.append((i1,i2))

    return big_list







def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into jquery_home (link,title) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass











#
if __name__ == '__main__':
    for offset in range(1,150):
        url = 'http://www.htmleaf.com/jQuery/list_1_' + str(offset) + '.html'
        html = get_one_page(url)
        content = parse_page(html)
        insertDB(content)
        print(datetime.datetime.now())


#
# create table jquery_home(
#     id int not null primary key auto_increment,
# link text,
# title text
# ) engine=Innodb  charset=utf8;
#
# #
# drop table ctolib_python_links_details;
