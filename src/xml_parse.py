#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-03-27 19:10
# @Author   : San
# @Project  : Malaysian-Character-Knowledge-Graph
# @File     : xml_parse.py
# @Software : PyCharm
# @Desc     :


from src.base import XMLParser

xml_parser = XMLParser(filter_categories=['Orang hidup'], category='Kategori')

xml_parser.parse_file_block('../ms_wiki_data/mswiki-20210120-pages-articles-multistream.xml')
xml_parser.save('../ms_wiki_data/ms_person_data.json')
