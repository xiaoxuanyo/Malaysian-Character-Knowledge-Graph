# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 18:49
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import json
from src.utils import LoggerUtil
import logging

_FILE_LOG_LEVEL = logging.INFO

_file_log = LoggerUtil('src.analyse.file', file_path='../log/analyse.log',
                       level=_FILE_LOG_LEVEL, mode='w+')


class Analyse:

    def __init__(self, path, encoding='utf-8'):
        with open(path, 'r', encoding=encoding) as f:
            data = json.load(f)
        self._nums = len(data)
        self._info_length = {j['title']: len(j.get('info', {}).keys()) for j in data.values()}

    @property
    def get_nums(self):
        return self._nums

    @property
    def get_info_nums(self):
        zero_num, one_num, two_num, bigger_num = 0, 0, 0, 0
        for i in self._info_length.values():
            if i == 0:
                zero_num += 1
            elif i == 1:
                one_num += 1
            elif i == 2:
                two_num += 1
            else:
                bigger_num += 1
        return {
            'zero': zero_num,
            'one': one_num,
            'two_num': two_num,
            'bigger': bigger_num
        }

    @property
    def get_zero_title(self):
        titles = []
        for i, j in self._info_length.items():
            if j == 0:
                titles.append(i)
        _file_log.logger.info(titles)
        return titles

    @property
    def get_max_length(self):
        return max(self._info_length.values())


if __name__ == '__main__':
    analyse = Analyse('../ms_wiki_data/ps.json')
    print(analyse.get_nums)
    print(analyse.get_info_nums)
    print(analyse.get_max_length)
