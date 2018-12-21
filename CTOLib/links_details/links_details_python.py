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
    patt = re.compile('<div class="m-l-sm m-t-xxs m-r-sm text-md font-bold">'+
                      '.*?<a href="(.*?)">(.*?)</a>',re.S)
    items = re.findall(patt,html)
    for item in items:
        i1,i2 = item
        big_list.append(('https://www.ctolib.com'+i1,i2))
    return big_list
    #




def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into ctolib_python_links_details (link,title,DE) values (%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass











# url = 'https://www.ctolib.com/categories/python-databases-implemented-in-python-pg-4.html'
# html = get_one_page(url)
# content = parse_page(html)
# cn_insert2 = []
# for item2 in content:
#     i1, i2 = item2
#     cn_insert2.append((i1, i2, d_DE))
# print(cn_insert2)
# time.sleep(2)

#
if __name__ == '__main__':
#
#     # 使用cursor()方法获取操作游标
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    for i in range(1,48):
        sql = 'select * from ctolib_python_links where id = %s ' % i
        # #执行sql语句
        cursor.execute(sql)
        # #获取所有记录列表
        data = cursor.fetchone()
        d_link = data['link']
        d_DE = data['DE']
        for item1 in range(1, 16):
            url = d_link[:-5] + '-pg-' + str(item1) +'.html'
            html = get_one_page(url)
            content = parse_page(html)

            cn_insert2 = []
            for item2 in content:
                i1, i2 = item2
                cn_insert2.append((i1, i2, d_DE))
            insertDB(cn_insert2)
            time.sleep(1)



#







#
# create table ctolib_python_links_details(
#     id int not null primary key auto_increment,
# link text,
# title text,
# DE varchar(100)
# ) engine=Innodb  charset=utf8;
# #
# #
# drop table ctolib_python_links_details;
