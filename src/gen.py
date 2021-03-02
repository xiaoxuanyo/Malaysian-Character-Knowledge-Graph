# -*- coding: utf-8 -*-
"""
@time   : 2021-1-28 9:47
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import json
import mwparserfromhell as mwp
import pywikibot
from src.utils import LoggerUtil

"""
从所有人名词条title中获取Infobox数据并解析成字典格式（只要确保Infobox为字典形式即可），日志信息保存在gen.log
"""

MATCHES = 'Infobox'

_file_log = LoggerUtil(name='src.gen.file', file_path='../log/gen.log')
_console_log = LoggerUtil(name='src.gen.console')

with open('../ms_wiki_data/people.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

names = {i: j['title'] for i, j in data.items()}
site = pywikibot.Site('ms')
num = 0
all_num = len(names)

for i, j in names.items():
    try:
        page = pywikibot.Page(site, j)
        text = page.get(get_redirect=True)
        result = mwp.parse(text)
        tem = result.filter_templates(matches=MATCHES)
        data[i]['info'] = {}
        for k in tem:
            r_v = {str(p.name).strip(): str(p.value).strip() for p in k.params if
                   str(p.value).strip()}
            if r_v:
                data[i]['info'][str(k.name).strip()] = r_v
        with open('../ms_wiki_data/ps.json', 'w+', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=3)
        num += 1
        _console_log.logger.debug(f'[steps: {num} / {all_num}] [title: {j}] [id: {i}] [len: {len(tem)}]')
    except Exception as e:
        _file_log.logger.error(f'[steps: {num} / {all_num}] [title: {j}] [id: {i}] [wrong: {str(e)}]')
