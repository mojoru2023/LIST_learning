

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

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}



def get_one_page(url):
    req= requests.get(url,headers=headers)
      #  requests 中文编码的终极办法！
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding

        # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
        global encode_content
        encode_content = req.content.decode(encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
        return  (encode_content)



# 不用遍历url取代翻页！
def parse_page(html):
    seletor = etree.HTML(html)
    title = seletor.xpath("//div[@class='artlist clearfix']/dl/dt/a[@title]/text()")
    link = seletor.xpath("//div[@class='artlist clearfix']/dl/dt/a/@href")
    for i1,i2 in zip(title,link):
        yield (i1,'https://www.jb51.net'+i2)



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
        cursor.executemany('insert into scriptHome_linuxShell (title,link) values (%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass


if __name__ == '__main__':
    for offset in range(1,36):
        url = 'https://www.jb51.net/list/list_235_' + str(offset) + '.htm'
        html = get_one_page(url)
        content = parse_page(html)
        insertDB(content)
        time.sleep(1)
        print(datetime.datetime.now())








#
# create table scriptHome_linuxShell(
#     id int not null primary key auto_increment,
# title varchar(88),
# link varchar(66)
# ) engine=Innodb default charset=utf8;
# # #
# # #
# drop table scriptHome_python;
