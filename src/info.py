# -*- coding: utf-8 -*-
"""
@time   : 2021-1-28 10:58
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import json
import mwparserfromhell as mwp
from src.utils import LoggerUtil

_log = LoggerUtil(name='src.info.file', file_path='../log/info.log', mode='w+')
_console_log = LoggerUtil(name='src.info.console')

with open('../ms_wiki_data/ps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

tem = set()

for i, v in data.items():
    try:
        for name, value in v['info'].items():
            try:
                r = mwp.parse(name)
                r = r.filter_text(matches='Infobox')
                r = r[0]
                tem.add(str(r).strip().lower())
            except IndexError as e:
                _log.logger.error(f'[title: {v["title"]}] [id: {i}] [tem: {name}] [wrong: {str(e)}]')
    except KeyError:
        continue

tem = {i: set() for i in tem}

for v in data.values():
    if v.get('info'):
        for name, value in v['info'].items():
            r = mwp.parse(name)
            r = r.filter_text(matches='Infobox')
            if r:
                r = str(r[0]).strip().lower()
                for k in value.keys():
                    tem[r].add(k.lower())

tem = {i: list(j) for i, j in tem.items() if j}

with open('../ms_wiki_data/result.json', 'w+', encoding='utf-8') as f:
    json.dump(tem, f, ensure_ascii=False, indent=3)
