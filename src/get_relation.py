# -*- coding: utf-8 -*-
"""
@time   : 2021-3-17 17:50
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

from src.templates import TEMPLATE_MAP
import json

if __name__ == '__main__':
    values = set(TEMPLATE_MAP.values())

    name = []
    t_name = []
    multi_name = []
    t_multi_name = []
    _m_name = []
    _t_m_name = []
    ttt_name = {}
    for tem in values:
        for k, v in tem.fields_map.items():
            if not k.startswith('_'):
                if k not in name:
                    name.append(k)
                    t_name.append((k, list(v[0].values())[0]))
            else:
                if k not in _m_name:
                    _m_name.append(k)
                    _t_m_name.append((k, list(v[0].values())[0]))
        if tem.multi_values_field:
            for k, v in tem.multi_values_field.items():
                if k not in multi_name:
                    multi_name.append(k)
                    t_multi_name.append((k, list(v[0].values())[0]))
                ttt_name.update({k: []})

    for tem in values:
        for k, v in tem.fields_map.items():
            if not k.startswith('_'):
                if (k, list(v[0].values())[0]) not in t_name:
                    print(1, k, list(v[0].values())[0], tem.template_name)
            else:
                if (k, list(v[0].values())[0]) not in _t_m_name:
                    print(2, k, list(v[0].values())[0], tem.template_name)
        if tem.multi_values_field:
            for k, v in tem.multi_values_field.items():
                if (k, list(v[0].values())[0]) not in t_multi_name:
                    print(3, k, list(v[0].values())[0], tem.template_name)
                for ii in v[1]:
                    if ii not in ttt_name[k]:
                        ttt_name[k].append(ii)

    dic = {i[0]: i[1] for i in _t_m_name}

    a_dic = {i[0]: {'zh': i[1]} for i in t_name}

    b_dic = {}
    for i in t_multi_name:
        t = {}
        for k in ttt_name[i[0]]:
            try:
                zh = dic[k]
            except KeyError:
                zh = a_dic[k]['zh']
            t[k] = {'zh': zh}
        b_dic['(multi)' + i[0]] = {'inner_relation': t,
                                   'zh': i[1]}

    a_dic.update(b_dic)

    with open('../ms_wiki_data/relations.json', 'w+', encoding='utf-8') as f:

        json.dump(a_dic, f, indent=3, ensure_ascii=False)

    rl = {}
    for tem in values:
        name = tem.template_name
        rl[name] = {}
        test = {}
        for k, v in tem.fields_map.items():
            if not k.startswith('_'):
                rl[name].update({k: v[0]})
            else:
                test[k] = v[0]
        if tem.multi_values_field:
            for k, v in tem.multi_values_field.items():
                aa = {i: test.get(i, tem.fields_map[i][0]) for i in v[-1]}
                inner = {'inner_relation': aa}
                inner.update(v[0])
                rl[name].update({f'(multi){k}': inner})

    with open('../ms_wiki_data/template_relations.json', 'w+', encoding='utf-8') as f:

        json.dump(rl, f, indent=3, ensure_ascii=False)
