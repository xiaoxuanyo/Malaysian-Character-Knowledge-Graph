#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-03-27 19:10
# @Author   : San
# @Project  : Malaysian-Character-Knowledge-Graph
# @File     : test.py
# @Software : PyCharm
# @Desc     :

import json

with open('../ms_wiki_data/relations.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(len(data.keys()))
