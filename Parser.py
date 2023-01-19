# -*- coding: utf-8 -*-
# !/usr/local/bin/python3
"""
@File    : Article_Parser.py
@Author  : Gan Yuyang
@Time    : 2023/1/6 12:16
"""
import numpy as np
from bs4 import BeautifulSoup
import re

from wsj_selenium_crawler import lib
from source_crawler import cover_name
from lib import sep_print
from driver_init import Driver


def ab_char_sub(a: str):
    a = re.sub(r'[“”]', '"', a)
    a = re.sub(r"[‘’]", '', a)
    a = re.sub(r'，。', ',', a)
    a = re.sub(r'—', '-', a)
    a = re.sub(r'（', '(', a)
    a = re.sub(r'）', ')', a)
    a = re.sub(r'<a.*?>', '', a)
    a = re.sub(r'</a>', '', a)
    a = re.sub(r'<!-- -->', '', a)
    a = re.sub(r'<strong class.*?strong>', '', a)
    a = re.sub(r'<br.*?>', '', a)
    a = re.sub(r'<span.*?>', '', a)
    a = re.sub(r'</span>', '', a)
    a = re.sub(r'<svg.*?/svg>', '', a)
    return a


class ArticleParser(object):
    def __init__(self, soup):
        self.soup = soup

    def content(self):

        content = []
        body = str(self.soup.find_all('section')[0])
        # paras = body.find_all_next('p', attrs={'data-type': re.compile('paragraph')})
        # paras = body.find_all_next('p')
        paras = re.findall(r'<p.*?data-type.*?>(.*?)</p>', body)
        # sep_print(paras)
        # pattern = re.compile(r'<p.*?>([\w\d\s\.\,\—\(\)\"\'\:\?\!\…\-\%]+)')
        for p in paras[:len(paras) - 1]:
            a = str(p)
            #
            a = ab_char_sub(a)
            # print(a)
            #     para_content = pattern.findall(a)
            #     para_content = re.sub(r'')
            #     if para_content:
            #         content.append(para_content[0])
            content.append(a)

        return content

    def title(self):
        title_ = self.soup.find_all('title')[0]
        str_title = str(title_)

        str_title = ab_char_sub(str_title)
        pattern = re.compile(r'>([\w].*)<')
        article_title = re.findall(pattern, str_title)[0]
        return article_title

    def brief(self):
        brief_ = self.soup.find_all('h2')[0]
        str_brief = str(brief_)

        str_brief = ab_char_sub(str_brief)
        # print(str_brief)
        pattern = re.compile(r'>([\w].*)<')
        article_brief = re.findall(pattern, str_brief)[0]
        return article_brief

    def write_time(self):
        time_ = self.soup.find_all('time')
        str_time = str(time_)

        str_time = ab_char_sub(str_time)
        # print(str_time)
        try:
            data_time = re.findall(r'datetime="(.*?)T', str_time)[0]
        except Exception:
            data_time = ''
        return data_time


class LivecoverageParser(ArticleParser):
    def __init__(self, soup):
        ArticleParser.__init__(self, soup)
        self.soup = soup

    def content(self):
        content = []
        body = str(self.soup)
        paras = re.findall(r'<p>(.*?)</p>', body)[:-2]
        lis = re.findall(r'<li>(.*?)</li>', body)
        paras.extend(lis)
        for p in paras:
            p = ab_char_sub(p)
            content.append(p)

        return content

    def write_time(self):
        return ''


def parser_choser(type, soup):
    if type == 'articles':
        parser = ArticleParser(soup)
    elif type == 'livecoverage':
        parser = LivecoverageParser(soup)
    else:
        parser = None
    return parser


if __name__ == '__main__':
    driver = Driver(driver_path=lib.driver_path, extension_path=lib.ex_path).blank_driver()
    driver.get(
        'https://www.wsj.com/articles/the-disney-executive-who-made-119-505-a-day-11674045194?mod=hp_lead_pos9')
    lib.js_activator(driver)
    ps = driver.page_source
    # with open('6.html', 'w', encoding='utf-8') as f:
    #     f.write(ps)

    # with open('6.html', 'r', encoding='utf-8') as f:
    #     soup = BeautifulSoup(f, 'html.parser')
    # content(soup)
    # parser = ArticleParser(soup)
    # print(parser.title())
    # print(parser.brief())
    # print(parser.write_time())
    # parser.content()
    # sep_print(parser.content())

    soup = BeautifulSoup(ps, 'html.parser')
    parser = ArticleParser(soup)
    sep_print(parser.content())
