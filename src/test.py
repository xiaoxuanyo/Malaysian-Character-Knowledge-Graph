# -*- coding: utf-8 -*-
"""
@time   : 2021-1-27 15:54
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import re
a = r'birth.*?city|city.*?birth'


def _re_compile(s):
    s = s.split('|')
    _s = r'^'
    _e = r'\s*(\d*)$'
    s = [_s + i + _e for i in s]
    s = '|'.join(s)
    return re.compile(r'%s' % s)


print(re.search(_re_compile(a), 'birth city2').group())


aa = '{1}{0}'
print(aa.format(0, None))

