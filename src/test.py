#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-03-27 19:10
# @Author   : San
# @Project  : Malaysian-Character-Knowledge-Graph
# @File     : test.py
# @Software : PyCharm
# @Desc     :


from src.base import XMLParser

xml_parser = XMLParser()

print(xml_parser.parse_file('../ms_wiki_data/test.xml'))
