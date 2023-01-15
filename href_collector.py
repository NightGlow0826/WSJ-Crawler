#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : href_collector.py
@Author  : Gan Yuyang
@Time    : 2023/1/6 21:24
"""
# 处理wsj首页的内容
# 收集首页 主要新闻 的链接
from bs4 import BeautifulSoup
import re
from namer import Namer
# parsing the daily cover

from lib import sep_print


class Href_Collecter(object):
    def __init__(self):
        pass

    def lead_pos_href_list(self, file_name=None):
        if not file_name:
            file_name = Namer().cover_name()
        else:
            file_name = file_name
        with open(file_name, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        # soup = BeautifulSoup()
        a = soup.find_all('article')
        # sep_print(a)
        pattern = re.compile('"(http[s]*://.*?)"')
        hrefs = []
        lead_poses = []

        for article in a:
            cr = article.find_all_next('a', href=True)[0]
            cr = str(cr)
            # print(cr)
            hrefs.append(re.findall(pattern, cr)[0].replace('"', ''))

        for item in hrefs:
            if re.search('.*lead_pos.', item):
                lead_poses.append(item)

        return lead_poses


if __name__ == '__main__':
    name = Namer()
    hc = Href_Collecter()
    # hc.lead_pos_href_list(file_name=name.market_name())
    sep_print(hc.lead_pos_href_list(file_name=name.market_name()))
