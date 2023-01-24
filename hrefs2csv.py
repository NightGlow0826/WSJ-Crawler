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
from Parser import ArticleParser, LivecoverageParser, parser_choser, GooseParser
from lib import *
from namer import Namer
import lib
from bs4 import BeautifulSoup
from threading import Thread
from multiprocessing import Process
from pathos.multiprocessing import Pool


def list2df(href_list, df, retry=3):
    # want to try the muti-process
    series_lst = []

    def func(i, ):
        print('progress: {} of {}'.format(i + 1, len(href_list)), end='\t')
        print(href_list[i])

        for r in range(retry):
            driver = Driver(extension_path=ex_path).blank_driver(mute=True)
            driver.minimize_window()

            driver.get(href_list[i])
            time.sleep(2)
            js_activator(driver, thread_n=i + 1)

            # time.sleep(10 * (retry + 1))
            # pure_scroll(driver)
            # soup = BeautifulSoup(driver.page_source, 'html.parser')

            # with open('1.html', 'w+', encoding='utf-8') as f:
            #     f.write(driver.page_source)

            parser = GooseParser(driver.page_source)
            # time is actually not so important
            try:
                write_time = parser.write_time()
            except Exception:
                print('Thread {} write_time lost'.format(i + 1))
                write_time = ''

            try:
                title, brief, content, href = parser.title(), parser.brief(), parser.content(), \
                                              href_list[i]
                assert content
                assert brief

                df.loc[i] = [write_time, title, brief, content, href]

                print('Process {} success with retry: {}'.format(i + 1, r))
                # print(cover_df.loc[i])
                driver.quit()

                break
            except Exception:
                print('Process {} failed this time, retry {}'.format(i+1, r))
                time.sleep(3)
                if r < retry - 1:
                    driver.quit()
                    continue
                print('Retry{}, Process {} strange article form'.format(r + 1, i + 1))
                title, brief, write_time, content, href = '', '', '', '', \
                                                          href_list[i]
                df.loc[i] = [write_time, title, brief, content, href]
                driver.quit()

        print("Process {} done".format((i + 1)))
        # sep_print(content)

        time.sleep(0.5)
        return df.loc[i]

    p = Pool(4)
    for i in range(len(href_list)):
        # for i in range(2):
        s = p.apply_async(func, args=(i,))
        series_lst.append(s)

    p.close()
    p.join()

    print('sub process done')
    # print([i.get() for i in series_lst], '\n')
    # 先等进程结束， 不然会提前返回
    df_ = pd.DataFrame([i.get() for i in series_lst])
    return df_


class Extractor(object):
    def __init__(self, namer=Namer()):
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
        df = list2df(href_list, df, retry=3)
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


if __name__ == '__main__':
    hc = Href_Collecter()
    lib.net_check()
    namer = Namer()
    ex = Extractor()
    ex.cover(href_list=hc.lead_pos_href_list(namer.cover_name()))
    # ex.market(href_list=hc.lead_pos_href_list(namer.market_name()))
    # ex.quit()
