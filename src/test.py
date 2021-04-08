#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-03-27 19:10
# @Author   : San
# @Project  : Malaysian-Character-Knowledge-Graph
# @File     : test.py
# @Software : PyCharm
# @Desc     :


from src.base import XMLParser
from src.parse import Parser

xml_parser = XMLParser(filter_categories=['Orang hidup'], category='Kategori')

print(Parser.parse_wiki_data(data=xml_parser.parse_file('../ms_wiki_data/test.xml')['1040159']['info text'],
                             entry='test'))
