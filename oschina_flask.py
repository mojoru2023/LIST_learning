# -*- coding:utf8 -*-

# 写个小脚本就搞定了！
import re

import pymysql
import requests
import time
from requests.exceptions import ConnectionError
from selenium import webdriver

driver = webdriver.Chrome()


#请求

def get_first_page():
    url = 'https://www.oschina.net/search?scope=blog&q=flask&'
    # driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
    driver.set_window_size(1200, 1200)  # 设置窗口大小
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    return html


# 把首页和翻页处理？

def next_page():
    for i in range(1,58):  # selenium 循环翻页成功！
        print('第'+str(i) +'页')
        driver.find_element_by_xpath("//ul[@class='paging']/li[last()]").click()
        time.sleep(3)
        html = driver.page_source
        return html









# 用遍历打开网页59次来处理

    # print(html)  #正则还是有问题，选择了一个动态变动的颜色标记是不好的 最近浏览不是每次都有的！所以用数字的颜色取判断吧

def parse_html(html):

    patt = re.compile('<p class="url">(.*?)</p>',re.S)
    items = re.findall(patt, html)
    return items







#存储到MySQL中

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='flask_collections',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    try:
        cursor.executemany('insert into oschina (link) values (%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except StopIteration :
        pass

if __name__ == '__main__':
        html = get_first_page()
        content = parse_html(html)
        insertDB(content)
        while True:
            html = next_page()
            content = parse_html(html)
            insertDB(content)
        # print(offset)





# create table oschina(
# id int not null primary key auto_increment,
# link varchar(250)
# ) engine=InnoDB  charset=utf8;