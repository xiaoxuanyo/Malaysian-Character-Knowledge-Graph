# -*- coding: utf-8 -*-
"""
@time   : 2021-2-28 1:57
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import json
from tqdm import tqdm
import xml.sax
import io
import re
from src.base import QueryEngine, TemplateBase
from src.templates import TemplatePerson, TEMPLATE_MAP
import mwparserfromhell as mwp


class WikiContentHandler(xml.sax.handler.ContentHandler):
    InfoField = 'Infobox'

    def __init__(self, filter_categories=None, category=None, code='ms'):
        super(WikiContentHandler, self).__init__()
        self._buffer = ''
        self._current_tag = None
        self._per_page = {}
        self._code = code
        self.pages = {}
        if filter_categories is not None:
            assert category is not None, '指定filter_categories后，应提供对应语言的category。'
            assert isinstance(filter_categories, list), f'不支持的filter_categories类型{type(filter_categories)}，目前仅支持list类型。'
            split_tag = r'.*?[:：].*?'
            self._filter_categories = [category + split_tag + i for i in filter_categories]
        else:
            self._filter_categories = None

    @classmethod
    def _matches(cls, obj):
        if re.search(r'%s' % cls.InfoField, str(obj), re.I):
            return False
        return True

    def startElement(self, name, attrs):
        if name in ['title', 'text', 'id']:
            self._current_tag = name
        elif name == 'redirect':
            self._per_page['redirect title'] = attrs['title']

    def endElement(self, name):
        if name == self._current_tag:
            if not self._per_page.get(name):
                self._per_page[name] = self._buffer
            self._buffer = ''
            self._current_tag = None
        if name == 'page':
            if self._filter_categories is None or re.search(r'%s' % '|'.join(self._filter_categories),
                                                            self._per_page['text'], re.I):
                self._per_page['id url'] = 'https://%s.wikipedia.org/wiki?curid=%s' % (self._code, self._per_page['id'])
                self._per_page['title url'] = 'https://%s.wikipedia.org/wiki/%s' % (
                    self._code, self._per_page['title'].replace(' ',
                                                                '_'))
                self._per_page['all text'] = self._per_page.pop('text')
                self._per_page['info text'] = ''.join([str(i) for i in
                                                       mwp.parse(self._per_page['all text']).filter_templates(
                                                           matches=r'%s' % self.InfoField, recursive=False)])
                wiki_text = ''.join(
                    [str(i) for i in
                     mwp.parse(self._per_page['all text']).filter(matches=self._matches, recursive=False)])
                self._per_page['string text'] = ''.join([str(i) for i in TemplateBase.parse(wiki_text)]).strip(' ')
                if self._per_page.get('redirect title'):
                    self._per_page['redirect url'] = 'https://%s.wikipedia.org/wiki/%s' % (self._code, self._per_page[
                        'redirect title'].replace(' ', '_'))
                self._per_page = {k: v for k, v in self._per_page.items() if v}
                self.pages[self._per_page.pop('id')] = self._per_page
            self._per_page = {}

    def characters(self, content):
        if self._current_tag:
            self._buffer += content


class XMLParser:

    def __init__(self, filter_categories=None, category=None, code='ms'):
        self.handler = WikiContentHandler(filter_categories, category, code)
        self.parser = xml.sax.make_parser()
        self.parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        self.parser.setContentHandler(self.handler)
        self._input_source = None

    def parse_file(self, xml_file):
        self.parser.parse(xml_file)
        return self.handler.pages

    def parse_string(self, xml_string):
        if self._input_source is None:
            self._input_source = xml.sax.xmlreader.InputSource()
        if isinstance(xml_string, str):
            self._input_source.setCharacterStream(io.StringIO(xml_string))
        else:
            self._input_source.setByteStream(io.BytesIO(xml_string))
        self.parser.parse(self._input_source)
        return self.handler.pages

    def parse_file_block(self, xml_file):
        num = 0
        with open(xml_file, 'r', encoding='utf-8') as f:
            for _ in tqdm(f, desc='正在获取文件大小信息...', leave=False):
                num += 1
        with open(xml_file, 'r', encoding='utf-8') as f:
            for line in tqdm(f, desc='正在获取文件...', total=num):
                self.parser.feed(line)
        return self.handler.pages

    def save(self, path, encoding='utf-8'):
        with open(path, 'w+', encoding=encoding) as f:
            json.dump(self.handler.pages, f, ensure_ascii=False, indent=3)


class Parser:
    InfoField = 'Infobox'

    @staticmethod
    def _init(code, https_proxy=None):
        return QueryEngine(code, https_proxy)

    @classmethod
    def parse_wiki_data(cls, data, force=True, entry=None):
        """

        :param data: 必须是符合wiki语法格式的字符串
        :param force:
        :param entry:
        :return:
        """
        _props = []
        fields = {'template_name': [],
                  'entry': entry}
        default_temp = TemplatePerson if force else TemplateBase
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
    # http = '192.168.235.227:8888'
    # test = "{{Infobox actor\n|name = Normah Damanhuri \n|image = \n|image_size = \n|caption = \n|birth_name = \n|birth_date = {{birth date and age|1952|1|1}} \n|birth_place = [[Johor]], [[Persekutuan Tanah Melayu]] (kini [[Malaysia]])\n|occupation = Pelakon \n|years_active = 1980-an - kini\n|spouse = \n|children = {{plainlist|\n* Ahya Ulumuddin Rosli\n* Liana Rosli\n}}\n|relatives = [[Aripah Damanhuri]] (kakak)\n|parents = \n}}"
    # print(Parser.parse_wiki_data(test, entry='test'))
    # print(Parser.parse_wiki_title('Natalie Imbruglia', code='ms', http_proxy=http))

    # for i, j in fields_['fields'].items():
    #     for k in j['values']:
    #         print(f"{i}({list(j['relation_props'].values())[0]}): {k}\n")

    xml_parser = XMLParser(filter_categories=['Pilipino'], category='Kategorya', code='tl')

    xml_parser.parse_file_block('../ms_wiki_data/tlwiki-20201201-pages-articles-multistream.xml')
    xml_parser.save('../ms_wiki_data/tl_person_data.json')
