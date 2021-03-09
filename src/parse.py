# -*- coding: utf-8 -*-
"""
@time   : 2021-2-28 1:57
@author : xiexx
@email  : xiexx@xiaopeng.com
"""
import re

import mwparserfromhell as mwp

dont_parse = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading]
retain_template_name = (re.compile(r'medal'),)
discard_template_value = (['zh-hans'],)
retain_template_param = (['m', 'end', 'reason', 'award', 'ft', 'in', 'meter', 'meters',
                          'cm'], re.compile(r'\d+'))


def _matches(string, match):
    def match1(i_s, i_m):
        assert isinstance(i_m, list) or isinstance(i_m, re.Pattern), f'类型不符，match类型{type(i_m)}'
        if isinstance(i_m, list):
            if i_s in i_m:
                return True, None
            else:
                return False, None
        else:
            res = re.search(i_m, i_s)
            if res:
                return True, res
            else:
                return False, None

    def match2(i_s, m_l, m_r):
        assert isinstance(m_l, list) and isinstance(m_r,
                                                    re.Pattern), f'类型不符，match[0]类型{type(m_l)}，match[1]类型{type(m_r)}'
        if i_s in m_l:
            return True, None
        elif re.search(m_r, i_s):
            return True, re.search(m_r, i_s)
        else:
            return False, None

    assert isinstance(match, tuple), f'不支持的match类型{type(match)}'
    if len(match) == 1:
        return match1(string, match[0])
    elif len(match) == 2:
        if isinstance(match[0], dict):
            return match1(string, match[1])
        else:
            return match2(string, match[0], match[1])
    elif len(match) == 3:
        return match2(string, match[1], match[2])
    else:
        raise ValueError(f'不支持的match参数, {match}')


def parse(p_t):
    p_t = mwp.parse(p_t)
    p_t = p_t.filter(recursive=False)
    for i, j in enumerate(p_t):
        if isinstance(j, mwp.wikicode.Template):
            values = []
            for k in j.params:
                tag, res = _matches(k.name.strip_code().strip(' ').lower(), retain_template_param)
                if tag and not _matches(k.value.strip_code().strip(' ').lower(), discard_template_value)[0]:
                    if res:
                        values.append(k.value.strip_code().strip(' '))
                    else:
                        values.append(f"({k.name.strip_code().strip(' ')}: {k.value.strip_code().strip(' ')})")
            if _matches(j.name.strip_code().strip(' ').lower(), retain_template_name)[0]:
                res = f"({j.name.strip_code().strip(' ')}: {', '.join(values)})"
            else:
                res = ', '.join(values)
            p_t[i] = mwp.parse(res)
        elif isinstance(j, mwp.wikicode.ExternalLink):
            p_t[i] = j.url
        elif isinstance(j, mwp.wikicode.Tag):
            rs = mwp.parse('\n') if j.tag.strip_code().strip(' ') == 'br' else mwp.parse(
                j.contents.strip_code().strip(' '))
            p_t[i] = rs
        elif isinstance(j, mwp.wikicode.Wikilink):
            p_t[i] = mwp.parse(j.title.strip_code().strip(' '))
        elif isinstance(j, mwp.wikicode.HTMLEntity):
            p_t[i] = mwp.parse(j.normalize())
        elif any([isinstance(j, k) for k in dont_parse]):
            p_t[i] = mwp.parse(None)
    if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
        return p_t
    return parse(p_t)


def _re_compile(s, mode='se', split='.*?'):
    assert mode in ['s', 'e', 'se'], f'不支持{mode}'
    _s = r'^'
    _e = r'$'
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
        ss.append(r'\s*?(?P<s_index{}>\d*)\s*?'.format(j) + r'\D*?(?P<{}_index{}>\d*)\D*?'.join(i_split).format(
            *index) + r'\s*?(?P<e_index{}>\d*)\s*?'.format(j))
    s = ss
    s = '|'.join([_p.format(i, j) for j, i in enumerate(s)])
    print(s)
    return re.compile(r'%s' % s)


print(parse('https://ms.wikipedia.org/wiki/David_Boudia'))
