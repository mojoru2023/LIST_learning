#! -*- coding:utf-8 -*-
import re

from lxml import etree
from selenium import webdriver
import pymysql
import datetime
import time
driver = webdriver.Chrome()






def get_one_page(url):
    driver.get(url)
    html = driver.page_source
    driver.close()
    return html




def parse_page(html):
    big_list = []
    seletor = etree.HTML(html)
    title = seletor.xpath('//*[@id="wrap"]/div[2]/div//div/div/div/div[1]/text()[1]')
    title_f = []
    for item in title:
        title_f.append(item.strip())  #  字符串.strip()  为空默认剔除所有换行符,转义符号

    desc = seletor.xpath('//*[@id="wrap"]/div[2]/div//div/div/div/div[2]/text()[1]')
    desc_f = []
    for item in desc:
        desc_f.append(item.strip())
    link = seletor.xpath('//*[@id="wrap"]/div[2]/div//@href')
    for i1, i2,i3 in zip(title_f, desc_f,link):
        big_list.append((i1,i2,'https://www.ctolib.com'+i3))

    return big_list



def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into ctolib_linux_links (title,DE,link) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass




if __name__ == '__main__':
    url = 'https://www.ctolib.com/linux/categoriesallsub.html'
    html = get_one_page(url)
    content =parse_page(html)
    insertDB(content)












# #
# #
# create table ctolib_linux_links(
#     id int not null primary key auto_increment,
# title varchar(50),
# DE varchar(88),
# link varchar(180)
# ) engine=Innodb  charset=utf8;
# # #
# #
# drop table ctolib_python_links;
