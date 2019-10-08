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

import asyncio
import re
import logging
import aiohttp
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

titles = []
urls = []


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
    baseUrl = baseUrl[:22]
    for _tuple in result:
        url = baseUrl + _tuple[0]
        titles.append(_tuple[1])
        urls.append(url)


async def fetch(session, url):
    try:
        async with session.get(url, timeout=60) as response:
            return await response.text(encoding='gbk')
    except asyncio.TimeoutError:
        logging.error(f"{url} cannot get html information")
        return None

def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find_all(attrs={'id': 'content'})
    content = content[0].get_text()
    content = str(content).replace(u'\xa0\xa0\xa0\xa0', u'\n')
    content = str(content).replace(u'\xa0', u'')
    return content


async def section_crawl(f, start, step):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(start, start + step):
            if i >= len(titles):
                break
            task = fetch(session, urls[i])
            tasks.append(task)
        htmls = await asyncio.gather(*tasks)
    for i in range(start, start + step):
        if i > len(titles):
            break
        logging.info('start insert ' + titles[i])

        try:
            f.write(titles[i] + '\n')
            if htmls[i - start] is None:
                continue
            f.write(get_content(htmls[i-start]))
            f.write('\n\n')
        except Exception as e:
            logging.info(f"{len(htmls)}, {len(titles)}, {i-start}")
            logging.error(e)
            logging.error('{} insert failed!!'.format(titles[i]))
            continue


def main():
    url = "http://www.biqujia.com/book/5/5230/"
    getDirectory(url)
    if len(titles) != len(urls):
        return
    step = 10
    f = open("诡秘之主.txt", 'w')
    loop = asyncio.get_event_loop()
    for i in range(0, len(titles), step):
        logging.info(f"开始抓取{i}-{i+step}的章节")
        loop.run_until_complete(section_crawl(f, i, step))


from datetime import datetime as dt

if __name__ == '__main__':
    start = dt.now()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    main()
    logging.info(f"整个爬取过程共耗时 {dt.now() - start} s")
