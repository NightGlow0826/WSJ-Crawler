#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : crawler_main.py
@Author  : Gan Yuyang
@Time    : 2023/1/15 22:07
"""

from href_collector import Href_Collecter
from lib import *
import lib
from driver_init import Driver
from namer import Namer
from source_crawler import Crawler
from hrefs2csv import Extractor
from threading import Thread

def main():
    hc = Href_Collecter()
    namer = Namer()

    # 网络检查
    lib.net_check()

    # 爬取封面
    crawler = Crawler()
    th_cover, th_market = Thread(target=crawler.cover), Thread(target=crawler.market)

    th_cover.start(), th_market.start()
    th_cover.join(), th_market.join()


    # 分条爬取
    driver = Driver(extension_path=lib.ex_path).blank_driver()
    ex = Extractor(driver)
    ex.cover(href_list=hc.lead_pos_href_list(namer.cover_name()))
    ex.market(href_list=hc.lead_pos_href_list(namer.market_name()))


if __name__ == '__main__':
    main()
