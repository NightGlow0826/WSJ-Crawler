#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : namer.py
@Author  : Gan Yuyang
@Time    : 2023/1/7 18:04
"""
import datetime
from lib import mkdir
from pytz import timezone


class Namer(object):
    def __init__(self, time_zone='US/Eastern'):
        self.tz = time_zone

        if self.tz:
            date = datetime.datetime.now(tz=timezone(self.tz))
        else:
            date = datetime.datetime.now()
        self.Y, self.M, self.D = str(date.year), '_' + str(date.month), '_' + str(date.day)

    def cover_name(self, f_type: str = 'html', name=None):
        # 对封面源码文件进行明明
        if name:
            return name
        # tz = 'US/Eastern'
        path = './source/cover/' + f_type + '/'
        mkdir(path)
        daily_coversourse_filename = path + self.Y + self.M + self.D + '_cover.' + f_type
        return daily_coversourse_filename

    def market_name(self, f_type: str = 'html', name=None):
        if name:
            return name
        path = './source/market/' + f_type + '/'
        mkdir(path)
        daily_marketsourse_filename = path + self.Y + self.M + self.D + '_market.' + f_type
        return daily_marketsourse_filename



if __name__ == '__main__':
    name = Namer()
    print(name.cover_name(f_type='csv'))
