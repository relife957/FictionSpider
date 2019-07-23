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
import aiohttp
import asyncio
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


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text(encoding='gbk')


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all(attrs={'id': 'content'})
    content = content[0].get_text()
    content = str(content).replace(u'\xa0\xa0\xa0\xa0', u'\n')
    content = str(content).replace(u'\xa0', u'')
    return content


async def main():
    url = "http://www.biqujia.com/book/0/202/"
    directory = getDirectory(url)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for item in directory.items():
            tasks.append(fetch(session, item[1]))
        htmls = await asyncio.gather(*tasks)

    titles = list(directory.keys())
    if len(titles) == len(htmls):
        size = len(titles)
        with open('剑来.txt', 'w')as f:
            for i in range(size):
                print('start insert ' + titles[i])
                try:
                    f.write(titles[i] + '\n')
                    f.write(get_content(htmls[i]))
                    f.write('\n\n')
                except Exception as e:
                    print(e)
                    print('{} insert failed!!'.format(titles[i]))
                    continue


from datetime import datetime as dt

if __name__ == '__main__':
    start = dt.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print(dt.now() - start)
