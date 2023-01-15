#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : testq.py
@Author  : Gan Yuyang
@Time    : 2023/1/8 12:11
"""
import re

import pandas as pd
from namer import Namer
pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)
pd.set_option('max_colwidth', 500)

# with open('source/cover/2023_1_11_cover.csv', 'r', encoding='utf-8') as f:
#     a = f.read()
#     print(a)
namer = Namer()
df = pd.read_csv(namer.cover_name(f_type='csv'), header=0, index_col=0)
# print(df)

# df['title'] = df.title.map(lambda x: re.sub('- WSJ', '', x))

print(df)
