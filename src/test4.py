# -*- coding: utf-8 -*-
"""
@time   : 2021-2-28 1:57
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

a = ['number.*?of.*?films']
s = [list(range(1, len(i.split('.*?')) + 1))
     for j, i in enumerate(a)]
print(s)
