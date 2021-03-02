# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 18:49
@author : xiexx
@email  : xiexx@xiaopeng.com
"""
import json

from tqdm import tqdm

from src.templates import TEMPLATE_MAP, MULTI_DICT, TEST
from src.utils import LoggerUtil
import logging

_file_log = LoggerUtil('src.analyse.file', file_path='../log/analyse.log',
                       level=logging.INFO, mode='w+')

with open('../ms_wiki_data/ps.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in tqdm(data.values(), '正在构建知识图谱...'):
    if i.get('info'):
        for k, v in i['info'].items():
            tem = TEMPLATE_MAP.get(k.lower().strip())
            if tem:
                template = tem(v, i['title'], multi_dict=MULTI_DICT)

_file_log.logger.info(MULTI_DICT)
_file_log.logger.info(TEST)
