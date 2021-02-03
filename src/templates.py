# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 13:42
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import mwparserfromhell as mwp
import pywikibot

__all__ = ['Template', 'TemplateEngineer', 'TemplateChineseActorSinger']


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


def _is_int(ind):
    try:
        int(ind)
        return True
    except ValueError:
        return False


class TemplateBase:
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
        'Website': ['website', 'url'],
        'Origin': ['origin'],
        'Religion': ['religion', 'agama'],
        'Education': ['education'],
        'Occupation': ['occupation', 'occupation(s)', 'pekerjaan'],
        'Years Active': ['year_active', 'yearsactive', 'years active', 'years_singing', 'years_active'],
        'Death Date': ['death_date'],
        'Spouse': ['spouse'],
        'Parents': ['parents']
    }

    _dont_parse = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading]

    def __init__(self, values, entry=None):
        self.fields = {k: [] for k in self.fields_map.keys()}
        for k, v in values.items():
            field = self._reverse_fields_map.get(k.strip())
            if field:
                p_v = self.parse(v.strip())
                print(field, ': ', ''.join([str(i) for i in p_v]))
                print('\n')
                self.fields[field].append(''.join([str(i) for i in p_v]))
        if entry is not None:
            self.fields['Entry'] = [entry]
        self.fields = {k: v for k, v in self.fields.items() if v}

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
                    p_t[i] = mwp.parse(None)
            elif any([isinstance(j, k) for k in cls._dont_parse]):
                p_t[i] = mwp.parse(None)
        if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
            return p_t
        return cls.parse(p_t)

    @property
    def graph_tuple(self):
        result = []
        if self.fields.get('Entry'):
            entry = self.fields.pop('Entry')[0]
        else:
            entry = self.fields['Name'][0]
        for k, v in self.fields.items():
            for i in v:
                result.append((entry, k, i))
        return result


class TemplateEngineer(TemplateBase):
    fields_map = {
        'Discipline': ['discipline'],
        'Institutions': ['institutions'],
        'Practice Name': ['practice_name'],
        'Significant Projects': ['significant_projects'],
        'Significant Awards': ['significant_awards']
    }

    fields_map.update(TemplateBase.fields_map)
    _reverse_fields_map = {i: k for k, v in fields_map.items() for i in v}


class TemplateChineseActorSinger(TemplateBase):
    fields_map = {
        'Traditional Chinese Name': ['tradchinesename'],
        'Pinyin Chines Name': ['pinyinchinesename'],
        'Simplified Chinese Name': ['simpchinesename'],
        'Music Type': ['genre'],
        'Record Company': ['label'],
        'Musical Instrument': ['instrument'],
        'Influenced': ['influenced'],
        'Awards': ['hongkongfilmwards', 'ntsawards', 'awards',
                   'tvbanniversaryawards', 'mtvasiaawards',
                   'goldenhorseawards', 'goldenroosterawards',
                   'goldenbauhiniaawards', 'goldenmelodyawards'],
        'Associated Artists': ['associatedact'],
        'Partner': ['partner'],
        'Voice Type': ['voicetype'],
        'Chinese Name': ['chinesename']
    }
    fields_map.update(TemplateBase.fields_map)
    _reverse_fields_map = {i: k for k, v in fields_map.items() for i in v}


class Template(TemplateBase):
    _all = [TemplateEngineer, TemplateChineseActorSinger]

    fields_map = {}

    for t in _all:
        fields_map.update(t.fields_map)
    _reverse_fields_map = {i: k for k, v in fields_map.items() for i in v}


