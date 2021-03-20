# -*- coding: utf-8 -*-
"""
@time   : 2021-2-28 1:57
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

from src.base import QueryEngine, TemplateBase
from src.templates import TemplatePerson, TEMPLATE_MAP
import mwparserfromhell as mwp


class Parse:
    InfoField = 'Infobox'

    @staticmethod
    def _init(code, https_proxy=None):
        return QueryEngine(code, https_proxy)

    @classmethod
    def parse_wiki_data(cls, data, force=True, entry=None):
        """

        :param data: pywikibot.Page().get()对象或者是已简单解析的dict对象
        :param force:
        :param entry:
        :return:
        """
        _props = []
        fields = {'template_name': [],
                  'entry': entry}
        default_temp = TemplatePerson if force else TemplateBase
        if isinstance(data, dict):
            class DicTTemp:
                class InnerTemp:
                    class InnerParams:
                        def __init__(self, name, value):
                            self.name = name
                            self.value = value

                    def __init__(self, name, value):
                        self.name = name
                        self.params = [self.InnerParams(ii, jj) for ii, jj in value.items()]

                def __init__(self, d):
                    self.d = d
                    self.keys = list(d.keys())
                    self._pop = list(range(len(self.keys)))

                def pop(self, index):
                    key = self.keys[index]
                    self._pop.pop(self._pop.index(index))
                    value = self.d[key]
                    return self.InnerTemp(key, value)

                def __iter__(self):
                    return self

                def __next__(self):
                    if self._pop:
                        index = self._pop[0]
                        return self.pop(index)
                    else:
                        raise StopIteration

            temp = DicTTemp(data)
        else:
            data = mwp.parse(data)
            temp = data.filter_templates(matches=cls.InfoField)
        if temp:
            tem = temp.pop(0)

            values = {str(p.name).strip(' '): str(p.value).strip(' ') for p in
                      tem.params if
                      str(p.value).strip(' ')}
            template = TEMPLATE_MAP.get(str(tem.name).strip(' ').lower(), default_temp)
            res = template(values, entry)
            if res.template_name not in fields['template_name']:
                fields['template_name'].append(res.template_name)
            fields['fields'] = res.fields['fields']
            if res.fields.get('primary_entity_props'):
                if res.fields['primary_entity_props']['multi_values_field'] not in _props:
                    _props.append(res.fields['primary_entity_props']['multi_values_field'])
            for t in temp:
                values = {str(p.name).strip(' '): str(p.value).strip(' ') for p
                          in
                          t.params if
                          str(p.value).strip(' ')}
                template = TEMPLATE_MAP.get(str(t.name).strip(' ').lower(), default_temp)
                res = template(values, entry)
                if res.template_name not in fields['template_name']:
                    fields['template_name'].append(res.template_name)
                for i, j in res.fields['fields'].items():
                    if i not in fields['fields'].keys():
                        fields['fields'][i] = j
                    else:
                        for k in j['values']:
                            if k not in fields['fields'][i]['values']:
                                fields['fields'][i]['values'].append(k)
                if res.fields.get('primary_entity_props'):
                    if res.fields['primary_entity_props']['multi_values_field'] not in _props:
                        _props.append(res.fields['primary_entity_props']['multi_values_field'])
            if _props:
                fields['primary_entity_props'] = {'multi_values_field': '\n'.join(_props)}
            return fields
        else:
            return None

    @classmethod
    def parse_wiki_title(cls, title, code, http_proxy=None, force=True, get_redirect=False):
        """
        :param title: 条目
        :param code:
        :param http_proxy:
        :param force:
        :param get_redirect:
        :return:
        """
        query = cls._init(code, http_proxy)
        data = query.get_wiki_page(title, get_redirect, force=False)
        return cls.parse_wiki_data(data, force, title)

    @classmethod
    def parse_values(cls, values, template_name=None, entry=None, force=True):
        """

        :param values: 键值对待解析的值
        :param template_name: 用什么模板解析
        :param entry:
        :param force:
        :return:
        """
        default_temp = TemplatePerson if force else TemplateBase
        if template_name is not None:
            template_name = template_name.strip(' ').lower()
        temp = TEMPLATE_MAP.get(template_name, default_temp)
        res = temp(values, entry)
        return res.fields


if __name__ == '__main__':
    http = '192.168.235.227:8888'
    print(Parse.parse_wiki_title('Ryan Gosling', code='ms', http_proxy=http))
