# -*- coding: utf-8 -*-
"""
@time   : 2021-2-28 1:57
@author : xiexx
@email  : xiexx@xiaopeng.com
"""
import re

import mwparserfromhell as mwp

_dont_parse = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading]


def _is_int(ind):
    try:
        int(ind)
        return True
    except ValueError:
        return False


def parse(p_t):
    p_t = mwp.parse(p_t)
    p_t = p_t.filter(recursive=False)
    for i, j in enumerate(p_t):
        if isinstance(j, mwp.wikicode.Template):
            values = []
            for k in j.params:

                # if not _is_int(str(k.name)):
                #     if str(k.name).strip() not in TEST['test']:
                #         TEST['test'].append(str(k.name).strip())

                if _is_int(str(k.name).strip(' ')) and str(k.value).strip(' ') not in ['zh-hans']:
                    values.append(str(k.value).strip(' '))
                elif str(k.name).strip(' ') in ['m', 'end', 'reason', 'award', 'ft', 'in', 'meter', 'meters', 'cm']:
                    values.append(f"({str(k.name).strip(' ')}: {str(k.value).strip(' ')})")
            p_t[i] = mwp.parse(', '.join(values))
        elif isinstance(j, mwp.wikicode.ExternalLink):
            p_t[i] = j.url
        elif isinstance(j, mwp.wikicode.Tag):
            rs = mwp.parse('\n') if str(j.tag) == 'br' else mwp.parse(str(j.contents).strip(' '))
            p_t[i] = rs
        elif isinstance(j, mwp.wikicode.Wikilink):
            p_t[i] = mwp.parse(str(j.title).strip(' '))
        elif isinstance(j, mwp.wikicode.HTMLEntity):
            p_t[i] = mwp.parse(j.normalize())
        elif any([isinstance(j, k) for k in _dont_parse]):
            p_t[i] = mwp.parse(None)
    if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
        return p_t
    return parse(p_t)


def _re_compile(s, mode='se', split='.*?'):
    assert mode in ['s', 'e', 'se'], f'不支持{mode}'
    _s = r'^'
    _e = r'\s*(?P<e_index{}>\d*)$'
    if mode == 's':
        _p = _s + '{}'
    elif mode == 'e':
        _p = '{}' + _e
    else:
        _p = _s + '{}' + _e
    s = s.split('|')
    ss = []
    for j, i in enumerate(s):
        i_split = i.split(split)
        index = []
        for k in range(len(i_split)):
            index.append('i' + str(j))
            index.append(str(j + k))
        ss.append(r'\D*?(?P<s_index{}>\d*)\D*?'.format(j) + r'\D*?(?P<{}_index{}>\d*)\D*?'.join(i_split).format(*index))
    s = ss
    s = '|'.join([_p.format(i, j) for j, i in enumerate(s)])
    return re.compile(r'%s' % s)

