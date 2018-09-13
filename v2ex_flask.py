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
    patt = re.compile('<td width="auto" valign="middle"><span class="item_title"><a href="(.*?)">(.*?)</a></span>')
    items = re.findall(patt,html)
    for item in items:
        small_list = list(item)
        link = 'https://www.v2ex.com' + small_list[0]
        title = small_list[1]
        yield link,title




#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into v2ex_flask (link,title) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass

if __name__ == '__main__':
    for offset in range(1,11):

        url = 'https://www.v2ex.com/go/flask?p=' + str(offset)
        html = call_page(url)
        content = parse_page(html)
        insertDB(content)
        print(offset)

# create table v2ex_flask(
# id int not null primary key auto_increment,
# link varchar(125),
# title varchar(160)
# ) engine=InnoDB  charset=utf8;