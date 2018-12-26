#! -*- coding:utf-8 -*-
import re
import urllib

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
    link =  selector.xpath("/html/body/div/div[2]/div//div[1]/figure/img/@src")
    for i1,i2 in zip(title,link):
        urllib.request.urlretrieve(i2,'/home/lk/jquery_home/%s.jpg' % i1)




#
if __name__ == '__main__':
    for offset in range(1,150):
        url = 'http://www.htmleaf.com/jQuery/list_1_' + str(offset) + '.html'
        html = get_one_page(url)
        parse_page(html)
        print(datetime.datetime.now())




