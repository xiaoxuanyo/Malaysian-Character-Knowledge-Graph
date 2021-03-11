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


def get_fields(all_template):
    fields = set()
    multi_fields = set()
    gen_fields = set()
    multi_fields2 = set()
    for tem in all_template:
        for i in tem.fields_map.keys():
            if i.startswith('_'):
                multi_fields.add(i)
            else:
                fields.add(i)
        if tem.multi_values_field:
            for k, v in tem.multi_values_field.items():
                gen_fields.add(k)
                for j in v[-1]:
                    multi_fields2.add(j)
    return fields, multi_fields, gen_fields, multi_fields2


if __name__ == '__main__':
    template = ['infobox_politician']
    key = 'branch'
    print(get_keys(template, key))
