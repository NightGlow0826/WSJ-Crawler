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
from threading import Thread


def list2df(href_list, df, ):
    # want to try the muti-thread
    def func(i, df=df, ):
        print('progress: {} of {}'.format(i + 1, len(href_list)), end='\t')
        print(href_list[i])
        driver = Driver(extension_path=ex_path).blank_driver(mute=True)
        driver.get(href_list[i])
        js_activator(driver)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # with open('1.html', 'w+', encoding='utf-8') as f:
        #     f.write(driver.page_source)

        parser = parser_choser(essay_type(href_list[i]), soup)
        try:
            title, brief, write_time, content, href = parser.title(), parser.brief(), parser.write_time(), parser.content(), \
                                                      href_list[i]
            df.loc[i] = [write_time, title, brief, content, href]
            # print('Thread {} strange article form'.format(i+1))


        except Exception:
            print('Thread {} strange article form'.format(i+1))
            title, brief, write_time, content, href = '', '', '', '', \
                                                      href_list[i]
            df.loc[i] = [write_time, title, brief, content, href]
        # driver.quit()

        print("Thread {} done".format((i+1)))
        # sep_print(content)

        time.sleep(0.5)


    thread_lst = [Thread(target=func, args=(i, )) for i in range(len(href_list))]
    # thread_lst = [Thread(target=func, args=(i, )) for i in range(2)]
    for thread in thread_lst:
        thread.start()
    for thread in thread_lst:
        thread.join()
    # 先等进程结束， 不然会提前返回
    # print(df)
    return df


class Extractor(object):
    def __init__(self, driver, namer=Namer()):
        self.driver = driver
        self.namer = namer

    def cover(self, href_list, name: str = None):
        df = pd.DataFrame({
            "write_time": [],
            "title": [],
            "brief": [],
            "content": [],
            "href": []
        })
        if not name:
            name = self.namer.cover_name(f_type='csv')
        df = list2df(href_list, df, )
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
        df = list2df(href_list, df, )

        if not name:
            name = self.namer.market_name(f_type='csv')
        df.to_csv(name, sep=',', index=True, header=True)
        return True

    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    hc = Href_Collecter()
    lib.net_check()
    namer = Namer()
    driver = Driver(extension_path=lib.ex_path).blank_driver()
    ex = Extractor(driver)
    # ex.cover(href_list=hc.lead_pos_href_list(namer.cover_name()))
    ex.market(href_list=hc.lead_pos_href_list(namer.market_name()))
    # ex.quit()
