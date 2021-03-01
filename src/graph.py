#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-02-03 22:45
# @Author   : San
# @Project  : character_knowledge_graph
# @File     : graph.py
# @Software : PyCharm
# @Desc     :


from src.templates import TEMPLATE_MAP
from py2neo import Graph, Node, Relationship
from tqdm import tqdm
import json


class KnowledgeGraph:

    def __init__(self, host, username, password, delete=True):
        self.graph = Graph(host, username=username, password=password)
        if delete:
            self.graph.delete_all()

    def insert(self, data):
        if not self.graph.nodes.match(data['node_label'], name=data['node_name']).exists():
            node = Node(data['node_label'], name=data['node_name'])
            self.graph.create(node)
        node1 = self.graph.nodes.match(data['node_label'], name=data['node_name']).first()
        for i in data['node_relation']:
            tag = False
            if not self.graph.nodes.match(name=i[1]).exists():
                tag = True
                node = Node('others', name=i[1])
                self.graph.create(node)
            if not tag:
                node2 = self.graph.nodes.match(name=i[1]).first()
            else:
                node2 = self.graph.nodes.match('others', name=i[1]).first()
            try:
                pr = i[2]
            except IndexError:
                pr = {}
            if not self.graph.relationships.match((node1, node2), r_type=i[0], **pr).exists():
                relation = Relationship(node1, i[0], node2, **pr)
                self.graph.create(relation)


if __name__ == '__main__':
    graph = KnowledgeGraph("http://localhost:7474", username="neo4j", password="XXX981110")
    with open('../ms_wiki_data/ps.json', 'r', encoding='utf-8') as f:
        j_data = json.load(f)

    for i in tqdm(j_data.values(), '正在构建知识图谱...'):
        if i.get('info'):
            for k, v in i['info'].items():
                tem = TEMPLATE_MAP.get(k.lower().strip())
                if tem:
                    template = tem(v, i['title'])
                    graph.insert(template.graph_entities)

