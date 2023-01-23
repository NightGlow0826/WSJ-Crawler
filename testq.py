#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""
@File    : testq.py
@Author  : Gan Yuyang
@Time    : 2023/1/8 12:11
"""
import re
import pandas as pd

df1 = pd.DataFrame({
            "write_time": [],
            "title": [],
            "brief": [],
            "content": [],
            "href": []
        })

df2 = pd.DataFrame({
            "write_time": [],
            "title": [],
            "brief": [],
            "content": [],
            "href": []
        })
df1.loc[1] = 1, 2, 3, 4, 5
df2.loc[2] = 6, 7, 8, 9, 0
df3 = pd.DataFrame([df1.loc[1], df2.loc[2]])
print(df3)


