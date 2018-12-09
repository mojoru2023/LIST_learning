# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql
import requests



#请求

def call_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'}
    response = requests.get(url,headers=headers)
    return response.text


# 解析

def parse_page(html):
    patt = re.compile('<a href="(.*?)" target="_blank" strategy="SearchFromCsdn"><em>Flask</em>(.*?)</a>')
    items = re.findall(patt,html)
    for item in items:
        yield (item[0],item[1])

#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into csdn_flask (link,title) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass

if __name__ == '__main__':
    for offset in range(1,76):

        url = 'https://so.csdn.net/so/search/s.do?p='+ str(offset) + '&q=flask&t=blog&domain=&o=&s=&u=&l=&f=&rbg=0'
        html = call_page(url)
        content = parse_page(html)
        insertDB(content)
        print(offset)

# create table csdn_flask(
# id int not null primary key auto_increment,
# link varchar(250),
# title varchar(50)
# ) engine=InnoDB  charset=utf8;