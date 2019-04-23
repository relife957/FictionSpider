# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     UU
   Description :
   Author :       wangyi
   date：          4/4/19
-------------------------------------------------
   Change Activity:
                   4/4/19:
-------------------------------------------------
"""
import re

__author__ = 'wangyi'


import requests
from prettyprinter import pprint
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'fcip=111; ASP.NET_SessionId=yt3vz5yaca4ofazdbx3k5spo; _ga=GA1.2.1066683067.1554340954; _gid=GA1.2.1240436335.1554340954; __atssc=google%3B2; lastread=289%3D95002%3D%u7B2C%u4E00%u7AE0%20%u9B47%u9B54%u5C9B; __atuvc=3%7C14; __atuvs=5ca55c5a5c3b23e5002',
    'Host': 'www.uukanshu.com',
    'Referer': 'https://www.google.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
def getHtml(url):
    try:
        request = requests.get(url,headers=headers)
        if request.status_code != 200 :
            return request.status_code

        request.encoding = 'gb2312'
        html = request.text

    except :
        html = ""
    return html

def getDirectory(baseUrl):
    html = getHtml(baseUrl)
    pattern = "<li><a href=\"(.*).html\" .*>(.*)</a>"
    result = re.findall(pattern, html)

    directory = []
    for tumple in result:
        url = baseUrl + tumple[0][9:]+".html"
        directory.append((tumple[1],url))

    return directory

def getContent(url):
    html = getHtml(url)
    soup = BeautifulSoup(html,'lxml')
    tag = soup.find_all(attrs={'class':'contentbox'})[0]

    pattern = re.compile('[\u4e00-\u9fa5\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b]+')
    content = re.findall(pattern,tag.text)

    return content


def write(filename,list):
    with open(filename,'w') as f:
        for line in list:
            f.write(line)
            if line.endswith('。') or line.endswith('!') or line.endswith('"') or line.endswith('?') or line.endswith('.'):
                f.write('\n')

def main():
    url = "https://www.uukanshu.com/b/62531/"
    directory = getDirectory(url)
    directory.reverse()
    # pprint(directory)
    with open("./牧神记.txt",'w') as f:
        for li in directory:
            try:
                f.write(li[0]+'\n')
                print(li[0])
                content = getContent(li[1])
                for line in content:
                    f.write(line)
                    if line.endswith('。') or line.endswith('!') or line.endswith('"') or line.endswith(
                            '?') or line.endswith('.'):
                        f.write('\n')
            except Exception as e:
                print(li[0]+" "+li[1])
                continue





if __name__ == '__main__':
    main()