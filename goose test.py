#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : goose test.py
@Author  : Gan Yuyang
@Time    : 2023/1/22 21:50
"""
import re

from goose3 import Goose
from driver_init import Driver
from wsj_selenium_crawler import lib
from lib import *
from dateutil.parser import *
from Parser import ab_char_sub
g = Goose()

# driver = Driver(extension_path=lib.ex_path).blank_driver()
#
# url = r'https://www.wsj.com/articles/more-classified-documents-found-at-bidens-delaware-home-11674346611?mod=hp_lead_pos2'
# driver.get(url)
# js_activator(driver)
# with open('6.html', 'w+', encoding='utf-8') as f:
#     f.write(driver.page_source)

with open('6.html', 'r', encoding='utf-8') as f:


    article = g.extract(raw_html=f.read())



    print(article.title)
    print(article.meta_description)
    write_time = article.publish_date.replace('\n', '')
    write_time = re.sub(r'ET(.*)', '', write_time)
    write_time = re.sub(r'.*Updated\s', '', write_time)

    print(write_time)
    print(parse(write_time).date())
    a = article.cleaned_text
    b = a.split()
    a = ' '.join(b)
    a = ab_char_sub(a)
    print(a)


