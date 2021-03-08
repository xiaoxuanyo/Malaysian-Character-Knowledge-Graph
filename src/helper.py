# -*- coding: utf-8 -*-
"""
@time   : 2021-3-4 15:27
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import json

with open('../ms_wiki_data/ps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def get_keys(templates, keys):
    values = []
    templates = [i.lower() for i in templates]
    for v in data.values():
        if v.get('info'):
            vv = {kkk.lower(): vvv for kkk, vvv in v.get('info').items()}
            for j in templates:
                if vv.get(j):
                    vvv = {kkk.lower(): vvv for kkk, vvv in vv.get(j).items()}
                    if vvv.get(keys):
                        values.append(v['title'])
    return values


if __name__ == '__main__':
    template = ['infobox sportsperson']
    key = 'collegeteam'
    print(get_keys(template, key))
