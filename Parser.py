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
import dateutil.parser


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
        for p in paras[:len(paras) - 1]:
            p = ab_char_sub(p)
            content.append(p)

        return content

    def write_time(self):
        return ''


class AMPParser(ArticleParser):
    def __init__(self, soup):
        ArticleParser.__init__(self, soup)
        self.strsoup = str(soup)
        self.soup = soup

    def title(self):
        h1_ = re.findall(r'<h1.*?>(.*?)</h1>', self.strsoup)[0]
        return h1_

    def brief(self):
        h2_ = re.findall(r'<h2.*?>(.*?)</h2>', self.strsoup)[0]
        return h2_

    def content(self):
        content = []
        body = self.soup.find_all('section')
        body_ = str(body)
        paras = re.findall(r'<p>(.*?)</p>', body_)
        for p in paras[:len(paras) - 1]:
            p = ab_char_sub(p)
            content.append(p)
        return content

    def write_time(self):
        time_ = self.soup.find_all('time')[0]
        str_time = str(time_)
        # print(str_time)
        str_time = ab_char_sub(str_time)
        str_time = re.sub(r'[\t|\n|\.|,]', ' ', str_time)

        # print(str_time)
        try:
            data_time = re.findall(r'Updated\s(.*?\d{4})', str_time)[0]
            t = data_time.split()
            a, m, d = t[2], t[0], t[1]

            data_time = str(dateutil.parser.parse(a + '.' + m + '.' + d))
            data_time = re.findall(r'(\d{4}.*?)\s', data_time)[0]
        except Exception:
            data_time = ''
        return data_time


def parser_choser(type, soup):
    if type == 'articles':
        parser = ArticleParser(soup)
    elif type == 'livecoverage':
        parser = LivecoverageParser(soup)
    elif type == 'amp':
        parser = AMPParser(soup)
    else:
        parser = None
    return parser


if __name__ == '__main__':
    # driver = Driver(driver_path=lib.driver_path, extension_path=lib.ex_path).blank_driver()
    url = 'https://www.wsj.com/amp/articles/feds-bullard-sees-need-to-keep-up-rapid-pace-of-rate-increases-11674058442?mod=markets_lead_pos9'
    # driver.get(url)
    # lib.js_activator(driver)
    # ps = driver.page_source
    # with open('6.html', 'w', encoding='utf-8') as f:
    #     f.write(ps)

    with open('6.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        parser = parser_choser(lib.essay_type(url), soup)
        print(parser.title())
        print(parser.brief())
        print(parser.write_time())
        # parser.content()
        # sep_print(parser.content())
