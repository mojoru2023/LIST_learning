

import requests
from lxml import etree
from selenium import webdriver
import pymysql
import datetime
import time
# driver = webdriver.Chrome()
#
# def get_firs_page(url):
#     driver.get(url)
#     html = driver.page_source
#     time.sleep(3)
#     return html

import time
from requests.exceptions import ConnectionError
from selenium import webdriver
from lxml import etree
import datetime
driver = webdriver.Chrome()


def get_first_page(url):
    driver.get(url)
    # time.sleep(3)
    html = driver.page_source
    # time.sleep(3)
    return html


# 不用遍历url取代翻页！
def parse_page(html):
    seletor = etree.HTML(html)
    title = seletor.xpath('//*[@id="qa"]/section/div[2]/h2/a/text()')
    link = seletor.xpath('//*[@id="qa"]/section/div[2]/h2/a/@href')
    for i1,i2 in zip(title,link):
        return (i1,'https://segmentfault.com'+i2)



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
        cursor.executemany('insert into scriptHome_javascript (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass

url = 'https://segmentfault.com/t/flask/questions?type=votes&page=8'
html = get_first_page(url)
print(html)


# if __name__ == '__main__':
#     for offset in range(1,67):
#         url = 'https://segmentfault.com/t/flask/questions?type=votes&page=' + str(offset)
#         html = get_one_page(url)
#
#         content = parse_page(html)

        # insertDB(content)
        # time.sleep(1)
        # print(datetime.datetime.now())








#
# create table scriptHome_javascript(
#     id int not null primary key auto_increment,
# title varchar(88),
# link varchar(66)
# ) engine=Innodb default charset=utf8;
# # #
# # #
# drop table scriptHome_python;
