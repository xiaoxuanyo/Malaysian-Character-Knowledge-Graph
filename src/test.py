# -*- coding: utf-8 -*-
"""
@time   : 2021-3-17 17:50
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

from src.templates import TEMPLATE_MAP

values = set(TEMPLATE_MAP.values())

name = []
t_name = []
multi_name = []
t_multi_name = []
for tem in values:
    for k, v in tem.fields_map.items():
        if not k.startswith('_'):
            if k not in name:
                name.append(k)
                t_name.append((k, list(v[0].values())[0]))
    if tem.multi_values_field:
        for k, v in tem.multi_values_field.items():
            if k not in multi_name:
                multi_name.append(k)
                t_multi_name.append((k, list(v[0].values())[0]))

for tem in values:
    for k, v in tem.fields_map.items():
        if not k.startswith('_'):
            if (k, list(v[0].values())[0]) not in t_name:
                print(k, list(v[0].values())[0], tem.template_name)
    if tem.multi_values_field:
        for k, v in tem.multi_values_field.items():
            if (k, list(v[0].values())[0]) not in t_multi_name:
                print(k, list(v[0].values())[0], tem.template_name)


for n in t_multi_name:
    if n not in t_name:
        t_name.append(n)


with open('../ms_wiki_data/relations.json', 'w+', encoding='utf-8') as f:
    import json
    json.dump({'relations': t_name}, f, indent=3, ensure_ascii=False)



