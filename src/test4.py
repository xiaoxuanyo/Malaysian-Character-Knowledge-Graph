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
            values = [str(k.value) for k in j.params if _is_int(str(k.name))]
            p_t[i] = mwp.parse('-'.join(values))
        elif isinstance(j, mwp.wikicode.ExternalLink):
            p_t[i] = j.url
        elif isinstance(j, mwp.wikicode.Tag):
            rs = mwp.parse('\n') if str(j.tag) == 'br' else j.contents
            p_t[i] = rs
        elif isinstance(j, mwp.wikicode.Wikilink):
            p_t[i] = j.text if j.text else j.title
        elif isinstance(j, mwp.wikicode.HTMLEntity):
            p_t[i] = j.normalize()
        elif any([isinstance(j, k) for k in _dont_parse]):
            p_t[i] = mwp.parse(None)
    if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
        return p_t
    return parse(p_t)


a = "7 Mei 2008<br><small>Pemangku: 31 Disember 1999 - 7 Mei 2000</small>"

print(parse(a))


