# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     biquge
   Description :
   Author :       wangyi
   date：          2019/7/23
-------------------------------------------------
   Change Activity:
                   2019/7/23:
-------------------------------------------------
"""
__author__ = 'wangyi'

import requests
import re
from bs4 import BeautifulSoup
from prettyprinter import pprint


def getHtml(url):
    try:
        response = requests.get(url)
        response.encoding = 'gbk'
        html = response.text
    except:
        html = ""
    return html


def getDirectory(baseUrl):
    html = getHtml(baseUrl)
    pattern = "<dd><a href=\"(.*?)\">(.*?)</a></dd>"
    result = re.findall(pattern, html)
    directory = {}
    baseUrl = baseUrl[:22]
    for tumple in result:
        url = baseUrl + tumple[0]
        directory[tumple[1]] = url

    return directory


def getContent(url):
    html = getHtml(url)
    if html == "":
        return html
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all(attrs={'id': 'content'})
    return content[0].get_text()


def main():
    url = "http://www.biqujia.com/book/0/202/"
    directory = getDirectory(url)
    with open("./剑来.txt", 'w',encoding='utf-8') as f:
        for item in directory.items():
            try:
                print(item[0])
                f.write(item[0] + '\n')
                content = getContent(item[1])
                content = content.replace(u'\xa0\xa0\xa0\xa0', u'\n')
                f.write(content)
                f.write('\n')
            except:
                print("error at " + str(item))
                continue
    # url = 'http://www.biqujia.com/book/0/202/11224.html'
    # content = getContent(url)
    # content = content.replace(u'\xa0\xa0\xa0\xa0', u'\n')
    # with open('剑来.txt','w',encoding='utf-8')as f:
    #     f.write(content)
    # pprint(content)
if __name__ == '__main__':
    main()
