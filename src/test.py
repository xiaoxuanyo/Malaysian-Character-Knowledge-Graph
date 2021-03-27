#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-03-27 19:10
# @Author   : San
# @Project  : Malaysian-Character-Knowledge-Graph
# @File     : test.py
# @Software : PyCharm
# @Desc     :

import re

string = 'Amit Deshmukh (adik)\n Dheeraj Deshmukh (adik)'
string = string.split('\n')
string = [i.strip() for i in string]
patten = re.compile(r'\((?P<front>.+?)\)\s*$|$\s*\((?P<after>.+?)\)')
string = [re.search(patten, i).groups() for i in string]
print(string)
