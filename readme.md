# 使用selenium爬取wsj

## 说明
这是构建 NLP&Finance 的语料库爬虫，目前日更可利用 crawle_main 获取

## 步骤
先把拓展的文件夹在浏览器开发者模式里打包成crx

1. 使用 driver_init 获得初始的webdriver
2. 使用 source_crawler 获取大页面的html源码
3. 利用 Namer 命名, 储存大页面源码至source文件夹
4. 使用 href_collector 获取大页面上文章的超链接

[//]: # (5. 使用 article_ori_code 输入超链接获取 文章页面源码)
6. 使用 Parser 获取 标题, 日期, 简介, 内容
7. 保存至csv

## 注意
1. 请使用clash等代理, 可以不加proxy参数
2. 谨防webrtc泄露
3. 记得把拓展路径加上去

