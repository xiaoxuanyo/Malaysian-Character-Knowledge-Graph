# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 13:42
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import mwparserfromhell as mwp
import pywikibot
from src.utils import LoggerUtil
import logging
import re

__all__ = ['TemplateEngineer', 'TemplateChineseActorSinger', 'QueryEngine',
           'TEMPLATE_MAP']

TEMPLATE_MAP = {}
_FILE_LOG_LEVEL = logging.DEBUG
_CONSOLE_LOG_LEVEL = logging.DEBUG

_file_log = LoggerUtil('src.templates.file', file_path='../log/templates.log',
                       level=_FILE_LOG_LEVEL, mode='w+')
_console_log = LoggerUtil('src.templates.console', level=_CONSOLE_LOG_LEVEL)


def _is_int(ind):
    try:
        int(ind)
        return True
    except ValueError:
        return False


class QueryEngine:

    def __init__(self, code, https_proxy=None):
        self.site = pywikibot.Site(code)
        if https_proxy is not None:
            import os
            os.environ['HTTPS_PROXY'] = https_proxy

    def get_wiki_page(self, title, get_redirect=False, force=False):
        page = pywikibot.Page(self.site, title)
        return page.get(get_redirect=get_redirect, force=force)

    def get_info_template(self, title, matches, get_redirect=False, force=False):
        text = self.get_wiki_page(title, get_redirect=get_redirect, force=force)
        ps = mwp.parse(text)
        return ps.filter_templates(matches=matches)


class TemplateBase:
    template_name = 'Base'
    fields_map = {
        'Name': ['name', 'nama'],
        'Alias': ['alias', 'othernames', 'other_names', 'others name', 'others_name', 'othername'],
        'Native Name': ['native_name'],
        'Birth': ['birth'],
        'Birth Name': ['birth_name', 'birth name', 'birthname'],
        'Birth Date': ['birth_date', 'born', 'birthdate'],
        'Birth Place': ['birth_place', 'tempat lahir', 'birthplace'],
        'Height': ['height'],
        'Weight': ['weight'],
        'Nationality': ['nationality'],
        'Website': ['website', 'url', 'homepage'],
        'Origin': ['origin'],
        'Religion': ['religion', 'agama'],
        'Education': ['education', 'pendidikan'],
        'Occupation': ['occupation', 'occupation(s)', 'pekerjaan'],
        'Years Active': ['year_active', 'yearsactive', 'years active', 'years_singing', 'years_active', 'active'],
        'Death Date': ['death_date'],
        'Spouse': ['spouse'],
        'Parents': ['parents'],
        'Children': ['children'],
        'Gender': ['gender'],
        'Alma Mater': ['alma_mater'],
        'Location': ['location'],
        'Relatives': ['relatives']
    }

    _dont_parse = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading]

    def __init__(self, values, entry):
        self._fields = {'template_name': self.template_name,
                        'fields': {k: [] for k in self.fields_map.keys()},
                        'entry': entry}
        for k, v in values.items():
            field = None
            for kk, vv in self.fields_map.items():
                if isinstance(vv, list):
                    if k.lower().strip() in vv:
                        field = kk
                        break
                elif isinstance(vv, re.Pattern):
                    if re.search(vv, k.lower().strip()):
                        field = kk
                        break
                else:
                    raise TypeError(f'不支持的类型: {type(vv)}')
            if field:
                p_v = self.parse(v.strip())
                _console_log.logger.debug(f'\n{field}: {"".join([str(i) for i in p_v])}\n')
                self._fields['fields'][field].append(''.join([str(i) for i in p_v]))
        self._fields['fields'] = {k: v for k, v in self._fields['fields'].items() if v}

    @classmethod
    def parse(cls, p_t):
        p_t = mwp.parse(p_t)
        p_t = p_t.filter(recursive=False)
        for i, j in enumerate(p_t):
            if isinstance(j, mwp.wikicode.Template):
                values = [str(k.value) for k in j.params if _is_int(str(k.name))]
                p_t[i] = mwp.parse('-'.join(values))
            elif isinstance(j, mwp.wikicode.ExternalLink):
                p_t[i] = j.url
            elif isinstance(j, mwp.wikicode.Tag):
                rs = mwp.parse('\n') if str(j.tag) == 'br' else j.contents
                p_t[i] = rs
            elif isinstance(j, mwp.wikicode.Wikilink):
                p_t[i] = j.text if j.text else j.title
            elif isinstance(j, mwp.wikicode.HTMLEntity):
                if str(j.value) == 'ndash':
                    p_t[i] = mwp.parse('-')
                else:
                    _file_log.logger.debug(f'[{str(j)}] [{str(j.value)}]')
                    p_t[i] = mwp.parse(None)
            elif any([isinstance(j, k) for k in cls._dont_parse]):
                p_t[i] = mwp.parse(None)
        if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
            return p_t
        return cls.parse(p_t)

    @property
    def fields(self):
        return self._fields


class TemplateEngineer(TemplateBase):
    template_name = 'Engineer'
    fields_map = {
        'Discipline': ['discipline'],
        'Institutions': ['institutions'],
        'Practice Name': ['practice_name'],
        'Significant Projects': ['significant_projects'],
        'Significant Awards': ['significant_awards']
    }

    fields_map.update(TemplateBase.fields_map)


class TemplateChineseActorSinger(TemplateBase):
    template_name = 'Chinese Actor And Singer'
    fields_map = {
        'Traditional Chinese Name': ['tradchinesename'],
        'Pinyin Chines Name': ['pinyinchinesename'],
        'Simplified Chinese Name': ['simpchinesename'],
        'Music Type': ['genre'],
        'Record Company': ['label'],
        'Musical Instrument': ['instrument'],
        'Related Influence': ['influenced', 'influences'],
        'Partner': ['partner'],
        'Voice Type': ['voicetype'],
        'Awards': re.compile(r'awards'),
        'Chinese Name': ['chinesename'],
        'Notable Role': ['notable role'],
        'Associated Artists': ['associatedact'],
        'Related Works': ['associated_acts', 'associated acts'],
        'Current Members': ['currentmembers'],
        'Past Members': ['pastmembers'],
        'English Name': ['nama inggeris']
    }
    fields_map.update(TemplateBase.fields_map)


if __name__ == '__main__':
    value = {
        "name": "Boram",
        "image": "Boram @ SC Showcase.jpg",
        "native_name": "전보람",
        "birth_name": "Jeon Boram",
        "alias": "Boram",
        "birth_date": "{{birth date and age|1986|03|22}}",
        "birth_place": "[[Seoul]], [[Korea Selatan]]",
        "parents": "[[Lee Mi-young]] {{small|(ibu)}}<br />Jeon Youngrok {{small|(bapa)}}",
        "relatives": "[[D-Unit|Jeon Wooram]] {{small|(adik perempuan)}}",
        "occupation": "{{flatlist|\n*[[Penyanyi]]\n*[[pelakon]]}}",
        "background": "solo_singer",
        "genre": "{{flatlist|\n*[[K-pop]]\n*[[J-pop]]\n*[[R&B]]\n*EDM\n*Electro-pop}}",
        "years_active": "2008–present",
        "label": "[[MBK Entertainment]]",
        "associated_acts": "{{hlist|[[T-ara]]|QBS}}",
        "URL": "{{url|http://www.mbk-ent.com/main_tara|T-ara}}"
    }
    template = TemplateChineseActorSinger(value, 'Jay Chou')
    print(template.fields)
