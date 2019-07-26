# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     飘天5
   Description :
   Author :       wangyi
   date：          4/23/19
-------------------------------------------------
   Change Activity:
                   4/23/19:
-------------------------------------------------
"""
__author__ = 'wangyi'

import requests
import re
from bs4 import BeautifulSoup
from prettyprinter import pprint


def getHtml(url):
    try:
        request = requests.get(url)
        html = request.text
    except:
        html = ""
    return html

def getDirectory(baseUrl):

    html = getHtml(baseUrl)
    pattern = "<dd><a href =\"(.*)\">(.*)</a></dd>"
    result = re.findall(pattern,html)
    result = result[6:]
    directory = {}
    baseUrl = baseUrl[:24]
    for tumple in result:
        url = baseUrl+tumple[0]
        directory[tumple[1]] = url

    return directory


def getContent(url):
    html = getHtml(url)
    if html == "":
        return html
    soup = BeautifulSoup(html,'lxml')
    content = soup.find_all(attrs={'class':'showtxt'})
    return content[0].get_text()



def main():
    url = "http://www.piaotian5.com/book/8339.html"
    directory = getDirectory(url)
    with open("./牧神记(2).txt",'w') as f:
        for item in directory.items():
            try:
                print(item[0])
                f.write(item[0]+'\n')
                content = getContent(item[1])
                f.write(content)
                f.write('\n')
            except:
                print(item)
                continue


if __name__ == '__main__':
    main()