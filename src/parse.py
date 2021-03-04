# -*- coding: utf-8 -*-
"""
@time   : 2021-2-28 1:57
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

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
            p_t[i] = mwp.parse(str(j.url).strip(' '))
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


a = "[[Lee Wan]] {{small| (adik lelaki)}}"

print(parse(a))
