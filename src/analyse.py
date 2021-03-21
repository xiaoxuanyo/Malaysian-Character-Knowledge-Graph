# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 18:49
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import json
from src.utils import LoggerUtil
import logging
from src.graph import KnowledgeGraph

_FILE_LOG_LEVEL = logging.INFO

_file_log = LoggerUtil('src.analyse.file', file_path='../log/analyse.log',
                       level=_FILE_LOG_LEVEL, mode='w+')


class Analyse:

    def __init__(self, path, encoding='utf-8', graph=None):
        with open(path, 'r', encoding=encoding) as f:
            data = json.load(f)
        self._nums = len(data)
        self._info_length = {j['title']: len(j.get('info', {}).keys()) for j in data.values()}
        self.graph = graph

    @property
    def nums(self):
        _file_log.logger.info(f'总数据量：{self._nums}')
        return self._nums

    @property
    def info_nums(self):
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
        res = {
            'zero': zero_num,
            'one': one_num,
            'two_num': two_num,
            'bigger': bigger_num
        }
        _file_log.logger.info(f'Infobox特征数量：{res}')
        return res

    @property
    def zero_title(self):
        titles = []
        for i, j in self._info_length.items():
            if j == 0:
                titles.append(i)
        _file_log.logger.info(f'Infobox为0的title：{titles}')
        return titles

    @property
    def max_num(self):
        res = max(self._info_length.values())
        _file_log.logger.info(f'含有最多Infobox的数量：{res}')
        return res

    @property
    def all_nodes_num(self):
        if self.graph is None:
            raise ValueError('graph is None!!!')
        res = len(self.graph.all_nodes)
        _file_log.logger.info(f'总节点数：{res}')
        return res

    @property
    def all_relations_num(self):
        if self.graph is None:
            raise ValueError('graph is None!!!')
        res = len(self.graph.all_relations)
        _file_log.logger.info(f'总关系数：{res}')
        return res


if __name__ == '__main__':
    g = KnowledgeGraph("http://localhost:7474", username="neo4j", password="XXX981110", delete=False)
    analyse = Analyse('../ms_wiki_data/ps.json', graph=g)
    analyse.nums
    analyse.info_nums
    analyse.max_num
    analyse.zero_title
    analyse.all_nodes_num
    analyse.all_relations_num
