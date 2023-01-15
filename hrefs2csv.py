#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : hrefs2csv.py
@Author  : Gan Yuyang
@Time    : 2023/1/11 16:58
"""

import pandas as pd
from href_collector import Href_Collecter
from driver_init import Driver
from Parser import ArticleParser, LivecoverageParser, parser_choser
from lib import *
from wsj_selenium_crawler import lib
from namer import Namer
from bs4 import BeautifulSoup


def list2df(href_list, df, driver):
    for i in range(len(href_list)):
        print('progress: {} of {}'.format(i + 1, len(href_list)), end='\t')
        print(href_list[i])
        driver.get(href_list[i])
        js_activator(driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # with open('1.html', 'w+', encoding='utf-8') as f:
        #     f.write(driver.page_source)

        parser = parser_choser(essay_type(href_list[i]), soup)
        title, brief, write_time, content, href = parser.title(), parser.brief(), parser.write_time(), parser.content(), \
                                                  href_list[i]
        # sep_print(content)
        df.loc[i] = [write_time, title, brief, content, href]

        time.sleep(0.5)

    return df


class Extractor(object):
    def __init__(self, driver):
        self.driver = driver

    def cover(self, href_list, name: str = None):
        df = pd.DataFrame({
            "write_time": [],
            "title": [],
            "brief": [],
            "content": [],
            "href": []
        })
        df = list2df(href_list, df, self.driver)
        if not name:
            name = namer.cover_name(f_type='csv')
        df.to_csv(name, sep=',', index=True, header=True)

        return True

    def market(self, href_list, name: str = None):
        df = pd.DataFrame({
            "write_time": [],
            "title": [],
            "brief": [],
            "content": [],
            "href": []
        })
        df = list2df(href_list, df, self.driver)

        if not name:
            name = namer.market_name(f_type='csv')
        df.to_csv(name, sep=',', index=True, header=True)
        return True

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    hc = Href_Collecter()
    lib.net_check()
    namer = Namer()
    driver = Driver(extension_path=lib.ex_path).blank_driver()
    ex = Extractor(driver).cover(href_list=hc.lead_pos_href_list(namer.cover_name()))
