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
    # Krystal Jung
    value = {
        "name": "Riteish Deshmukh",
        "image": "Riteish Deshmukh.jpg",
        "caption": "Deshmukh di acara filem ''[[Housefull]]'', 2010",
        "birth_name": "Ritesh Vilasrao Deshmukh",
        "birth_date": "{{Birth date and age|df=y|1978|12|17}}<ref name=\"ibti_Happ\">{{Cite web | title = Happy birthday Riteish Deshmukh: Rare photos and lesser known facts about 'Housefull 3' actor | last = Sen | first = Sushmita | work = International Business Times, India Edition | date = 16 December 2015 | accessdate = 2016-06-14 | url = http://www.ibtimes.co.in/happy-birthday-riteish-deshmukh-rare-photos-lesser-known-facts-about-housefull-3-actor-659789}}</ref><ref name=\"indi_Rite\">{{Cite web | title = Riteish Deshmukh turns 38, gets wishes galore from B-Town | author = IANS | work = The Indian Express | date = 17 December 2015 | accessdate = 2016-06-14 | url = http://indianexpress.com/article/entertainment/bollywood/riteish-deshmukh-turns-37-gets-wishes-galore-from-b-town/ }}</ref>",
        "birth_place": "[[Latur]],  [[Maharashtra]], [[India]]<ref name=\"gupta\">{{cite web|last=Gupta|first=Priya|title=Yes, Genelia is pregnant and we are both very excited about it: Ritesh Deshmukh|url=http://timesofindia.indiatimes.com/entertainment/hindi/bollywood/news-interviews/Yes-Genelia-is-pregnant-and-we-are-both-very-excited-about-it-Riteish-Deshmukh/articleshow/36150341.cms|website=Times of India|date=7 June 2014|accessdate=6 June 2014}}</ref>",
        "nationality": "[[India]]",
        "occupation": "Pelakon, pengacara, penerbit, arkitek",
        "years active": "2003–kini",
        "spouse": "[[Genelia D'Souza]] (k. 2012)",
        "children": "2",
        "parents": "{{plainlist|\n* [[Vilasrao Deshmukh]] (bapa)     \n* Vaishalitai Deshmukh (ibu)<ref name=\"Article4-914009\" >[https://web.archive.org/web/20120817122618/http://www.hindustantimes.com/photos-news/Photos-India/RememberingVilasraoDeshmukh/Article4-914009.aspx \"SRemembering Vilasrao Deshmukh\"]. ''Hindustan Times''.</ref>\n}}",
        "relatives": "{{plainlist|\n* [[Amit Deshmukh]] (adik)\n* Dheeraj Deshmukh (adik)\n}}"
    }
    # print(Parse.parse_wiki_title('Norodom Marie', code='ms', http_proxy=None))
    print(Parse.parse_values(value))
