# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     test
   Description :
   Author :       wangyi
   date：          2019/7/22
-------------------------------------------------
   Change Activity:
                   2019/7/22:
-------------------------------------------------
"""
__author__ = 'wangyi'

from pyquery import PyQuery as pq
import aiohttp
import asyncio
from prettyprinter import pprint


# def decode_html(html_content):
#     doc = pq(html_content)
#     des = ''
#     for li in doc.items("#phrsListTab .trans-container ul li"):
#         des += li.text()
#     return des
#
#
# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()
#
#
# async def main(words):
#     urls = ['http://dict.youdao.com/w/eng/{}'.format(word) for word in words]
#     tasks = []
#     async with aiohttp.ClientSession() as session:
#         for url in urls:
#             tasks.append(fetch(session, url))
#         htmls = await asyncio.gather(*tasks)
#         for html_content in htmls:
#             print(decode_html(html_content))

import time
async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")


if __name__ == '__main__':
    asyncio.run(main())
    # s = time.time()
    # text = 'apple'
    # words = text.split()
    # words = words * 100
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main(words))
    # print(time.time() - s)
