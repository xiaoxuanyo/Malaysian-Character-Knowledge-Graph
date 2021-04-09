# -*- coding: utf-8 -*-
"""
@time   : 2021-2-28 1:57
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

from src.base import QueryEngine, TemplateBase
from src.templates import TemplatePerson, TEMPLATE_MAP
import mwparserfromhell as mwp


class Parser:
    InfoField = 'Infobox'

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
            temp = cls.DicTTemp(data)
        else:
            data = mwp.parse(data)
            temp = data.filter_templates(matches=cls.InfoField)
        if temp:
            tem = temp.pop(0)
            values = {str(p.name).strip(): str(p.value) for p in
                      tem.params if
                      str(p.value)}
            template = TEMPLATE_MAP.get(str(tem.name).strip().lower(), default_temp)
            res = template(values, entry)
            if res.template_name not in fields['template_name']:
                fields['template_name'].append(res.template_name)
            fields['fields'] = res.fields['fields']
            if res.fields.get('primary_entity_props'):
                if res.fields['primary_entity_props']['multi_values_field'] not in _props:
                    _props.append(res.fields['primary_entity_props']['multi_values_field'])
            for t in temp:
                values = {str(p.name).strip(): str(p.value) for p
                          in
                          t.params if
                          str(p.value)}
                template = TEMPLATE_MAP.get(str(t.name).strip().lower(), default_temp)
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
                    for i_s in res.fields['primary_entity_props']['multi_values_field'].split('\n'):
                        if i_s not in _props:
                            _props.append(i_s)
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
            template_name = template_name.strip().lower()
        temp = TEMPLATE_MAP.get(template_name, default_temp)
        res = temp(values, entry)
        return res.fields


if __name__ == '__main__':
    http = '192.168.235.227:8888'
    test = {
         "Infobox person": {
            "name": "Dannii Minogue",
            "image": "Dannii Minogue arrives at the 58th Annual Logie Awards at Crown Palladium (26904220225) cropped.jpg",
            "caption": "Minogue di [[Melbourne]] pada 2016",
            "birth_name": "Danielle Jane Minogue",
            "birth_date": "{{Birth date and age|df=yes|1971|10|20}}",
            "birth_place": "[[Melbourne]], [[Victoria]], Australia",
            "occupation": "{{hlist|Penyanyi|penulis lagu|pelakon|model|personaliti televisyen|pereka fesyen}}",
            "years_active": "1979–kini",
            "spouse": "{{marriage|[[Julian McMahon]]<br />|1994|1995|end=div}}",
            "partner": "[[Jacques Villeneuve]]<br />({{abbr|bers.|bersama}} 1999; {{abbr|berp.|berpisah}} 2001)<ref>{{cite web|url=http://www.dannii.com.br/news/imagens/theage10.jpg |title=Archived copy |language=en |accessdate=21 Disember 2006 |url-status=dead |archiveurl=https://web.archive.org/web/20090326180303/http://www.dannii.com.br/news/imagens/theage10.jpg |archivedate=26 Mac 2009 }}</ref><br />[[Kris Smith]]<br />({{abbr|bers.|bersama}} 2008; {{abbr|berp.|berpisah}} 2012)",
            "children": "1",
            "relatives": "[[Kylie Minogue]] (kakak)",
            "module": "{{Infobox musical artist|embed=yes\n| background      = solo_singer\n| genre           = {{hlist|[[Pop]]|[[tarian]]}}\n| instrument      = Vokal\n| label           = {{hlist|[[Mushroom Records|Mushroom]]|[[MCA Records|MCA]]|[[Warner Music Group|Warner]]| [[London Records|London]]|[[Ultra Records|Ultra]]|[[All Around the World Productions|All Around the World]]}}\n| website         = {{URL|danniiminogue.com}}\n}}"
         }
      }
    print(Parser.parse_wiki_data(test, entry='test')['fields']['Partner']['values'])
    # print(Parser.parse_wiki_title('Natalie Imbruglia', code='ms', http_proxy=http))
    # print(Parse.parse_wiki_data(test))
    # print(RELATION)

    # fields_ = Parser.parse_wiki_title('Mike Gascoyne', code='ms', http_proxy=None)
    # print('\n\n\n\n', fields_)
    # for i, j in fields_['fields'].items():
    #     for k in j['values']:
    #         print(f"{i}({list(j['relation_props'].values())[0]}): {k}\n")
