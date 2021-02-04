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
        'Name': (['name', 'nama'],),
        'Alias': (['alias', 'othernames', 'other_names', 'others name', 'others_name', 'othername', 'othersname',
                   'other names', 'other_name', 'other name', 'other-names', 'others-name', 'other-name'],),
        'Native Name': (['native_name', 'native name', 'native-name'],),
        'Birth': (['birth'],),
        'Birth Name': (['birth_name', 'birth name', 'birthname', 'birth-name'],),
        'Birth Date': (
            ['birth_date', 'born', 'birthdate', 'birth date', 'date of birth', 'date  of birth', 'birth-date'],),
        'Birth Place': (['birth_place', 'tempat lahir', 'birthplace', 'birth place', 'place of birth', 'birth-place'],),
        'Height': (['height'],),
        'Weight': (['weight'],),
        'Nationality': (['nationality'],),
        'Website': (['website', 'url', 'homepage'],),
        'Origin': (['origin'],),
        'Religion': (['religion', 'agama'],),
        'Education': (['education', 'pendidikan'],),
        'Occupation': (['occupation', 'occupation(s)', 'pekerjaan'],),
        'Years Active': (['year_active', 'yearsactive', 'years active', 'years_active', 'active',
                          'yearactive', 'year active', 'year-active', 'years-active'],),
        'Death Date': (['death_date', 'death date', 'death-date'],),
        'Spouse': (['spouse'],),
        'Parents': (['parents'],),
        'Children': (['children', 'issue'],),
        'Gender': (['gender'],),
        'Alma Mater': (['alma_mater', 'alma mater', 'alma-mater'],),
        'Location': (['location'],),
        'Relatives': (['relatives'],),
        'Full Name': (['full name', 'full_name', 'full-name'],),
        'Father': (['father'],),
        'Mother': (['mother'],),
        'Residence': (['residence'],),
        'Known For': (['known_for', 'knownfor', 'known for', 'known-for'],),
        'Partner': (['partner'],),
        'Citizenship': (['citizenship'],),
        'Honorific Prefix': (['honorific-prefix', 'honorific prefix', 'honorificprefix',
                              'honorific_prefix'],),
        'Honorific Suffix': (['honorific-suffix', 'honorific suffix', 'honorificsuffix',
                              'honorific_suffix'],)
    }

    _dont_parse = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading]

    def __init__(self, values, entry):
        self._fields = {'template_name': self.template_name,
                        'fields': {k: [] for k in self.fields_map.keys()},
                        'entry': entry}
        for k, v in values.items():
            field = None
            for kk, vv in self.fields_map.items():
                assert isinstance(vv, tuple), f'fields map中的value为不支持的类型: {type(vv)}'
                if len(vv) == 1:
                    vvv = vv[0]
                    if isinstance(vvv, list):
                        if k.lower().strip() in vvv:
                            field = kk
                            break
                    elif isinstance(vvv, re.Pattern):
                        if re.search(vvv, k.lower().strip()):
                            field = kk
                            break
                    else:
                        raise TypeError(f'fields map中的value为不支持的类型: {type(vvv)}')
                elif len(vv) == 2:
                    v_l = vv[0]
                    v_r = vv[1]
                    assert isinstance(v_l, list) and isinstance(v_r,
                                                                re.Pattern), f'列表中的第一个为list枚举类型，第二个为正则表达式类型，目前的类型为: {type(v_l)}, {type(v_r)}'
                    if k.lower.strip() in v_l:
                        field = kk
                        break
                    if re.search(v_r, k.lower().strip()):
                        field = kk
                        break
                else:
                    raise ValueError('不支持的fields map类型')
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


class TemplateMotorcycleRider(TemplateBase):
    template_name = 'Motorcycle Rider'
    fields_map = {
        'Current Team': (['current team', 'current_team', 'currentteam', 'current-team'],),
        'Bike Number': (['bike number', 'bike_number', 'bikenumber', 'bike-number'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateEngineer(TemplateBase):
    template_name = 'Engineer'
    fields_map = {
        'Discipline': (['discipline'],),
        'Institutions': (['institutions'],),
        'Practice Name': (['practice_name', 'practice name', 'practice-name'],),
        'Significant Projects': (['significant_projects', 'significant projects', 'significant-projects'],),
        'Significant Awards': (['significant_awards', 'significant awards', 'significant-awards'],)
    }

    fields_map.update(TemplateBase.fields_map)


class TemplateChineseActorSinger(TemplateBase):
    template_name = 'Chinese Actor And Singer'
    fields_map = {
        'Traditional Chinese Name': (['tradchinesename'],),
        'Pinyin Chines Name': (['pinyinchinesename'],),
        'Simplified Chinese Name': (['simpchinesename'],),
        'Music Type': (['genre'],),
        'Record Company': (['label'],),
        'Musical Instrument': (['instrument'],),
        'Related Influence': (['influenced', 'influences'],),
        'Voice Type': (['voicetype', 'voice_type', 'voice type', 'voice-type'],),
        'Awards': (re.compile('awards'),),
        'Chinese Name': (['chinesename', 'chinese_name', 'chinese name', 'chinese-name'],),
        'Notable Role': (['notable role', 'notable_role', 'notable-role'],),
        'Associated Artists': (['associatedact', 'associated act', 'associated_act', 'associated-act'],),
        'Related Works': (['associated_acts', 'associated acts', 'associatedacts', 'associated-acts'],),
        'Current Members': (['currentmembers', 'current members', 'current_members', 'current-members'],),
        'Past Members': (['pastmembers', 'past_members', 'past members', 'past-members'],),
        'English Name': (['nama inggeris', 'nama_inggeris', 'namainggeris', 'nama-inggeris'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateRoyalty(TemplateBase):
    template_name = 'Royalty'
    fields_map = {
        'Successor': (['successor', 'heir'],),
        'House': (['house', 'residential', 'royal house', 'palace'],),
        'Reign': (['reign'],),
        'Coronation': (['coronation'],),
        'Predecessor': (['predecessor'],),
        'Succession': (['succession'],),
        'Regent': (['regent'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateModel(TemplateBase):
    template_name = 'Model'
    fields_map = {
        'Hair Color': (['haircolor', 'hair_color', 'hair color', 'haircolour', 'hair-color'],),
        'Eye Color': (['eyecolor', 'eye_color', 'eye color', 'eyecolour', 'eye-color'],),
        'Dress Size': (['dress size', 'dress_size', 'dresssize', 'dress-size'],),
        'Shoe Size': (['shoesize', 'shoe size', 'shoe_size', 'shoe-size'],),
        'Measurements': (['measurements'],),
        'Ethnicity': (['ethnicity'],),
        'Agency': (['agency'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateMinister(TemplateBase):
    template_name = 'Minister'
    fields_map = {
        'Office': (re.compile('office'),),
        'Prime Minister': (re.compile('prime.*?minister'),),
        'Party': (['party'],),
        'Term Start': (['term_start', 'termstart', 'term start', 'term-start'],),
        'Predecessor': (re.compile('predecessor'),)
    }
    fields_map.update(TemplateBase.fields_map)


_TEMPLATE_MAP = {
    TemplateMotorcycleRider: ['infobox motorcycle rider'],
    TemplateEngineer: ['infobox engineer'],
    TemplateChineseActorSinger: ['infobox chinese actor and singer',
                                 'infobox chinese-language singer and actor'],
    TemplateRoyalty: ['infobox royalty'],
    TemplateModel: ['infobox model']
}
TEMPLATE_MAP = {i: k for k, v in _TEMPLATE_MAP.items() for i in v}

if __name__ == '__main__':
    value = {
        "honorific-prefix": "[[Yang Amat Berhormat]]",
        "honorific-suffix": "[[Ahli parlimen|AP]]",
        "name": "Masagos Zulkifli <br> ماسڬوس ذوالكفل",
        "birth_name": "Masagos Zulkifli bin Masagos Mohamad",
        "image": "Masagos Zulkifli at The Pentagon, USA - 20061017.jpg",
        "caption": "Masagos pada makan tengah hari bekerja dianjurkan oleh Amerika Syarikat Setiausaha Pertahanan Donald Rumsfeld di Pentagon pada Oktober 2006",
        "office": "Menteri Pembangunan Sosial dan Keluarga Singapura",
        "primeminister": "[[Lee Hsien Loong]]",
        "term_start": "27 Julai 2020",
        "predecessor": "[[Desmond Lee]]",
        "office2": "[[Menteri Bertanggungjawab bagi Ehwal Masyarakat Islam]]",
        "primeminister2": "Lee Hsien Loong",
        "term_start2": "1 Mei 2018",
        "predecessor2": "[[Yaacob Ibrahim]]",
        "birth_date": "{{Birth date and age|1963|04|16|df=yes}}",
        "birth_place": "[[Koloni Singapura|Singapura]]",
        "party": "[[Parti Tindakan Rakyat]] (PAP)"
    }
    template = TemplateMinister(value, 'Jay Chou')
    print(template.fields)
