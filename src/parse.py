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

        :param data: pywikibot.Page().get()对象
        :param force:
        :param entry:
        :return:
        """
        fields = {'template_name': [],
                  'fields': {},
                  'entry': entry}
        default_temp = TemplatePerson if force else TemplateBase
        data = mwp.parse(data)
        temp = data.filter_templates(matches=cls.InfoField)
        for t in temp:
            template = TEMPLATE_MAP.get(str(t.name).strip(' ').lower(), default_temp)
            values = {str(p.name).strip(' '): str(p.value).strip(' ') for p in t.params if
                      str(p.value).strip(' ')}
            res = template(values, entry)
            if res.template_name not in fields['template_name']:
                fields['template_name'].append(res.template_name)
            fields['fields'].update(res.fields['fields'])
        return fields

    @classmethod
    def parse_wiki_title(cls, title, code, http_proxy=None, force=True, get_redirect=True):
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
    def parse_template(cls, values, template_name=None, entry=None, force=True):
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

