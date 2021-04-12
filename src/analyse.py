# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 18:49
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import json
from tqdm import tqdm
from src.parse import Parser
from src.utils import LoggerUtil
import logging

_FILE_LOG_LEVEL = logging.INFO

_file_log = LoggerUtil('src.analyse.file', file_path='../log/analyse1.log',
                       level=_FILE_LOG_LEVEL, mode='w+')

if __name__ == '__main__':
    INFO_DICT2 = {}
    t_num = 0
    num = 0
    with open('../ms_wiki_data/ms_person_data.json', 'r', encoding='utf-8') as f:
        j_data = json.load(f)

    for i in tqdm(j_data.values(), '正在构建知识图谱...'):
        t_num += 1
        if i.get('info text'):
            num += 1
            fields_all = Parser.parse_wiki_data(data=i['info text'], entry=i['title'])
            print(fields_all, '\n')
            for k, v in fields_all['fields'].items():
                INFO_DICT2[k + f"({v['relation_props']['zh']})"] = INFO_DICT2.get(k + f"({v['relation_props']['zh']})",
                                                                                  0) + 1
    INFO_DICT2 = {i: INFO_DICT2[i] for i in sorted(INFO_DICT2, key=INFO_DICT2.get, reverse=True)}
    print('\n\n', INFO_DICT2)
    _file_log.logger.info(json.dumps(INFO_DICT2, ensure_ascii=False, indent=3))
    _file_log.logger.info(f'total num: {t_num}')
    _file_log.logger.info(f'info num: {num}')
