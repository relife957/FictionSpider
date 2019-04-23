# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     笔趣阁
   Description :
   Author :       wangyi
   date：          1/20/19
-------------------------------------------------
   Change Activity:
                   1/20/19:
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
        request.encoding = 'gbk'
        html = request.text
    except :
        html = ""
    return html

def getDirectory(baseUrl):
    html = getHtml(baseUrl)
    pattern = "<li><a href=\"(.*)\">(.*)</a>"
    result = re.findall(pattern,html)

    directory = {}
    for tumple in result:
        url = baseUrl+tumple[0]
        directory[tumple[1]] = url

    return directory

def getContent(url):
    html = getHtml(url)
    if html == "":
        return ""
    soup = BeautifulSoup(html,'lxml')
    # content = soup.select('div[class="contentbox"]')
    content = soup.find_all(attrs={'id':'htmlContent'})
    return content[0].get_text()

def main():
    url =  "https://www.duquanben.com/xiaoshuo/22/22327/"
    directory = getDirectory(url)
    with open('./剑来.txt','w') as f:
        for k,v in directory.items():
            f.write('\n')
            f.write(k+'\n')
            print(k)
            content = getContent(v)
            t = content.split('\n')
            if len(t) < 1 :
                continue
            chapter = t[1]
            section = chapter.split(' ')
            for s in section:
                if s == '':
                    continue
                s = s.replace(r'\xa0','')
                f.write(s+'\n')

    # content = getContent("http://www.duquanben.com/xiaoshuo/6/6517/972960.html")
    # chapter = content.split("\n")[1]
    # section = chapter.split(' ')
    # # print(section)
    # with open('./test.txt','w')as f:
    #     for s in section:
    #         if s=='':
    #             continue
    #         s = s.replace(r'\xa0','')
    #         f.write(s+'\n')

if __name__ == '__main__':
    main()
