

import requests
from lxml import etree
from selenium import webdriver
import pymysql
import datetime
import time
driver = webdriver.Chrome()






def get_one_page(url):
    driver.get(url)
    html = driver.page_source
    return html

# 不用遍历url取代翻页！


def parse_page(self,html):
    self.html = html
    seletor = etree.HTML(html)
    title = seletor.xpath("//div[@class='artlist clearfix']/dl/dt/a[@title]/text()")
    link = seletor.xpath("//div[@class='artlist clearfix']/dl/dt/a/@href")
    for i1, i2 in zip(title, link):
        yield (i1, 'https://www.jb51.net' + i2)

# 不用遍历url取代翻页！

# def next_page():
#     for i in range(1,288):  # selenium 循环翻页成功！
#         driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div/div[3]/div[2]/a[last()-1]').click()
#         time.sleep(3)
#         html = driver.page_source
#         return html

def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='list_learning',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into scriptHome_ajax (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError:
        pass

url = 'https://www.ctolib.com'
html = get_one_page(url)
print(html)


# if __name__ == '__main__':
#     for offset in range(1,29):
#         url = 'https://www.jb51.net/list/list_5_' + str(offset) + '.htm'
#         html = get_one_page(url)
#         content = parse_page(html)
#         insertDB(content)
#         time.sleep(1)
#         print(datetime.datetime.now())








#
# create table scriptHome_ajax(
#     id int not null primary key auto_increment,
# title varchar(88),
# link varchar(66)
# ) engine=Innodb default charset=utf8;
# # #
# # #
# drop table scriptHome_python;
