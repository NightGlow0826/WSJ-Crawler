#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : source_crawler.py
@Author  : Gan Yuyang
@Time    : 2023/1/7 11:11
"""
import time
import lib
from driver_init import Driver
import datetime
from namer import Namer
from lib import mkdir, cover_name, js_activator

driver_path = lib.driver_path
ex_path = lib.ex_path
# proxies = lib.proxies

# 爬取整体页面源码
name = Namer()


class Crawler(object):
    def __init__(self, driver):
        self.driver = driver

    def cover(self):
        print('crawling cover_page')
        # 爬取封面源码
        self.driver.get('http://www.wsj.com')

        # 刷新js
        js_activator(driver=self.driver)

        # 现在是页面的源码了！

        with open(name.cover_name(), 'w+', encoding='utf-8') as f:
            f.write(driver.page_source)
        print('cover html successfully written')
        return True

    def market(self):
        print('crawling market_page')
        self.driver.get('https://www.wsj.com/news/markets?mod=nav_top_section')
        js_activator(driver=self.driver)

        with open(name.market_name(), 'w+', encoding='utf-8') as f:
            f.write(driver.page_source)
        print('market html successfully written')
        return True

if __name__ == '__main__':

    lib.net_check()

    driver = Driver(driver_path=driver_path, extension_path=ex_path).blank_driver()
    crawler = Crawler(driver)
    crawler.cover()
    crawler.market()
    driver.quit()

