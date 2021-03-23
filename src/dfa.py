# -*- coding: utf-8 -*-
"""
@time   : 2021-3-23 16:41
@author : xiexx
@email  : xiexx@xiaopeng.com
"""


class List(list):

    def __contains__(self, item):
        values = [i.value for i in self]
        if item in values:
            return True
        return False

    def __getitem__(self, item):
        instance = [i for i in self]
        values = [i.value for i in self]
        index = values.index(item)
        return instance[index]


class Node:

    def __init__(self):
        self.value = None
        self.children = None
        self.is_full = False


class DFA:

    def __init__(self):
        self.root = Node()

    def add_nodes(self, value):
        node = self.root
        for i in range(len(value)):
            node.value = value[i]
            if node.children is None:
                node.children = List([Node()])
            elif value[i] not in node.children:
                new_node = Node()
                new_node.value = value[i]
                node.children.append(new_node)
            node = node.children[value[i]]
        node.is_full = True

    def get_result(self, sentence):
        words = []
        indexes = []

        sent_len = len(sentence)

        for i in range(sent_len):

            p = self.root
            j = i
            tmp_flag = False
            word = None
            index = None

            while j < sent_len and p.children is not None and sentence[j] in p.children:
                p = p.children[sentence[j]]
                j = j + 1
                if p.is_full:

                    tmp_flag = True
                    word = sentence[i:j]
                    index = [i, j - 1]

            # if we find a node in dfa
            if tmp_flag:
                flag = False
                # if the indexes already contains words
                if len(indexes) > 0:

                    start, end = indexes[-1]
                    # if the word's first index bigger than the previous word's last index
                    # we add it
                    if i > end:
                        flag = True
                # if the indexes didn't contains any words
                else:
                    flag = True

                # put all the things into list
                if flag:
                    words.append(word)
                    indexes.append(index)
        return words, indexes


dfa = DFA()
dfa.add_nodes('你好啊')
dfa.add_nodes('不好啊')
print(dfa.get_result('你好啊，不好啊'))


