#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-02-03 22:45
# @Author   : San
# @Project  : character_knowledge_graph
# @File     : graph.py
# @Software : PyCharm
# @Desc     :
import logging
from py2neo import Graph, Node, Relationship
from tqdm import tqdm
import json
from src.parse import Parser
from src.base import RELATION
from src.utils import LoggerUtil

_FILE_LOG_LEVEL = logging.INFO

_file_log = LoggerUtil('src.graph.file', file_path='../log/graph.log',
                       level=_FILE_LOG_LEVEL, mode='w+')


class KnowledgeGraph:

    def __init__(self, host, username, password, delete=True):
        self.graph = Graph(host, username=username, password=password)
        if delete:
            self.graph.delete_all()

    def insert(self, fields):
        node1_label = '/'.join(fields['template_name'])
        node1_name = fields['entry']
        node1_props = fields.get('primary_entity_props', {})
        if not self.graph.nodes.match(name=node1_name).exists():
            node1 = Node(node1_label, name=node1_name, **node1_props)
            self.graph.create(node1)
        else:
            node1 = self.graph.nodes.match(name=node1_name).first()
        for k, v in fields['fields'].items():
            for item in v['values']:
                if not self.graph.nodes.match(name=item).exists():
                    node2 = Node('Others', name=item)
                    self.graph.create(node2)
                else:
                    node2 = self.graph.nodes.match(name=item).first()
                if not self.graph.relationships.match((node1, node2), r_type=k, **v['relation_props']).exists():
                    relation = Relationship(node1, k, node2, **v['relation_props'])
                    self.graph.create(relation)

    @property
    def all_nodes(self):
        print('正在获取节点...')
        nodes = self.graph.nodes.match().all()
        return nodes

    @property
    def all_relations(self):
        print('正在获取关系...')
        relations = self.graph.relationships.match().all()
        return relations


if __name__ == '__main__':
    # graph = KnowledgeGraph("http://localhost:7474", username="neo4j", password="XXX981110", delete=False)
    with open('../ms_wiki_data/ps.json', 'r', encoding='utf-8') as f:
        j_data = json.load(f)

    for i in tqdm(j_data.values(), '正在构建知识图谱...'):
        if i.get('info'):
            fields_all = Parser.parse_wiki_data(data=i['info'], entry=i['title'])
            print(fields_all, '\n')
            # graph.insert(fields_all)
    _file_log.logger.info(RELATION)
    with open('../ms_wiki_data/graph.json', 'w+', encoding='utf-8') as f:
        json.dump(RELATION, f, ensure_ascii=False, indent=3)
