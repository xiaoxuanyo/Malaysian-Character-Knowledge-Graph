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


def _re_compile(s):
    _s = r'^'
    _e = r'\s*\d*$'
    return re.compile(_s + s + _e)


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
        'Alias': (['alias', 'nickname'], _re_compile(r'other.*?names?')),
        'Native Name': (_re_compile(r'native.*?names?'),),
        'Birth': (['birth', 'born'],),
        'Birth Name': (_re_compile(r'birth.*?names?'),),
        'Birth Date': (_re_compile(r'birth.*?date|^date.*?birth'),),
        'Birth Place': (['tempat lahir'], _re_compile(r'birth.*?place|^place.*?birth')),
        'Birth City': (_re_compile(r'birth.*?city|^city.*?birth'),),
        'Birth Country': (_re_compile(r'birth.*?country|^country.*?birth'),),
        'Height': (['height'],),
        'Weight': (['weight'],),
        'Nationality': (['nationality'],),
        'Website': (['website', 'url', 'homepage'],),
        'Origin': (['origin'],),
        'Religion': (['religion', 'agama'],),
        'Education': (['education', 'pendidikan'],),
        'Occupation': (['occupation', 'occupation(s)', 'pekerjaan', 'ocupation', 'occuption',
                        'occuoation'],),
        'Years Active': (['active', 'yeaesactive'], _re_compile(r'year.*?active')),
        'Death Date': (_re_compile(r'death.*?date|^date.*?death'),),
        'Death Place': (_re_compile(r'death.*?place|^place.*?death'),),
        'Burial Place': (_re_compile(r'resting.*?place|^burial.*?place'),),
        'Spouse': (['spouse', 'pasangan'],),
        'Parents': (['parents'],),
        'Children': (['children', 'issue'],),
        'Gender': (['gender'],),
        'Alma Mater': (_re_compile(r'alma.*?mater'),),
        'Location': (['location'],),
        'Relatives': (_re_compile(r'relatives?|^relations?'),),
        'Full Name': (_re_compile(r'full.*?name'),),
        'Father': (['father', 'bapa'],),
        'Mother': (['mother'],),
        'Residence': (['residence'],),
        'Known For': (['known'], _re_compile(r'known.*?for'),),
        'Partner': (['partner'],),
        'Citizenship': (['citizenship'],),
        'Honorific Prefix': (_re_compile(r'honorific.*?prefix'),),
        'Honorific Suffix': (_re_compile(r'honorific.*?suffix'),),
        'Home Town': (_re_compile(r'home.*?town'),),
        'Employer': (['employer'],),
        'Leader': (_re_compile(r'leader'),),
        'Family': (['family'],),
        'Ethnicity': (['ethnicity', 'ethnic'],),
        'Subject': (['subject'],),
        'Works': (['works'],),
        'Net Worth': (_re_compile(r'net.*?worth'),),
        'Awards': (_re_compile(r'awards?'),),
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
                    if k.lower().strip() in v_l:
                        field = kk
                        break
                    elif re.search(v_r, k.lower().strip()):
                        field = kk
                        break
                else:
                    raise ValueError('不支持的fields map类型')
            if field:
                p_v = self.parse(v.strip())
                h_v = ''.join([str(i) for i in p_v]).strip()
                if h_v:
                    _console_log.logger.debug(f'\n{field}: {h_v}\n')
                    if h_v not in self._fields['fields']:
                        self._fields['fields'][field].append(h_v)
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
        'Current Team': (_re_compile(r'current.*?team'),),
        'Bike Number': (_re_compile(r'bike.*?number'),)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateEngineer(TemplateBase):
    template_name = 'Engineer'
    fields_map = {
        'Discipline': (['discipline'],),
        'Institutions': (['institutions'],),
        'Practice Name': (_re_compile(r'practice.*?names?'),),
        'Significant Projects': (_re_compile(r'significant.*?projects?'),),
        'Significant Awards': (_re_compile(r'significant.*?awards?'),)
    }

    fields_map.update(TemplateBase.fields_map)


class TemplateChineseActorSinger(TemplateBase):
    template_name = 'Chinese Actor And Singer'
    fields_map = {
        'Traditional Chinese Name': (['tradchinesename'],),
        'Pinyin Chines Name': (['pinyinchinesename'],),
        'Simplified Chinese Name': (['simpchinesename'],),
        'Genre': (['genre'],),
        'Record Company': (['label'],),
        'Instrument': (['instrument', 'instruments'],),
        'Influenced': (['influenced', 'influences'],),
        'Voice Type': (_re_compile(r'voice.*?type'),),
        'Chinese Name': (_re_compile(r'chinese.*?name'),),
        'Notable Role': (_re_compile(r'notable.*?roles?'),),
        'Associated Artists': (['associatedact', 'associated act', 'associated_act', 'associated-act'],),
        'Related Works': (['associated_acts', 'associated acts', 'associatedacts', 'associated-acts'],),
        'Current Members': (_re_compile(r'current.*?members?'),),
        'Past Members': (_re_compile(r'past.*?members?'),),
        'English Name': (_re_compile(r'nama.*?inggeris'),)
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
        'Hair Color': (['haircolour'], _re_compile(r'hair.*?color')),
        'Eye Color': (['eyecolour'], _re_compile(r'eye.*?color')),
        'Dress Size': (_re_compile(r'dress.*?size'),),
        'Shoe Size': (_re_compile(r'shoe.*?size'),),
        'Measurements': (['measurements'],),
        'Agency': (['agency'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateMinister(TemplateBase):
    template_name = 'Minister'
    fields_map = {
        'Office': (_re_compile(r'office'),),
        'Prime Minister': (_re_compile(r'prime.*?minister'),),
        'Party': (['party'],),
        'Term Start': (_re_compile(r'term.*?start'),),
        'Predecessor': (_re_compile(r'predecessor'),)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateOfficeholder(TemplateBase):
    template_name = 'Officeholder'
    fields_map = {
        'Office': (_re_compile(r'office'),),
        'Deputy': (_re_compile(r'deputy'),),
        'Term Start': (_re_compile(r'term.*?start'),),
        'Term End': (_re_compile(r'term.*?end'),),
        'Term': (_re_compile(r'term'),),
        'Predecessor': (_re_compile(r'predecessor'),),
        'Successor': (_re_compile(r'successor|^succeeded|^succeeding'),),
        'Prime Minister': (_re_compile(r'prime.*?minister'),),
        'Pronunciation': (['pronunciation'],),
        'President': (_re_compile(r'president'),),
        'Governor': (_re_compile(r'governor|^governor.*?general'),),
        'Serve With': (_re_compile(r'alongside'),),
        'Vice President': (_re_compile(r'vice.*?president'),),
        'Profession': (['profession'],),
        'Branch': (['branch'],),
        'Service Years': (_re_compile(r'service.*?years?'),),
        'Appointer': (_re_compile(r'appointer'),),
        'Minister': (_re_compile(r'minister'),),
        'Cabinet': (['cabinet'],),
        'Department': (['department'],),
        'Nominator': (_re_compile(r'nominator'),),
        'Chancellor': (_re_compile(r'chancellor'),),
        'Lieutenant': (_re_compile(r'"lieutenant"'),),
        'Appointed': (_re_compile(r'appointed'),)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateFootballPlayer(TemplateBase):
    template_name = 'Football Player'
    fields_map = {
        'Player Name': (_re_compile(r'player.*?name'),),
        'Current Club': (_re_compile(r'current.*?club'),),
        'Club Number': (_re_compile(r'club.*?number'),),
        'Position': (['position'],),
        'Years': (_re_compile(r'years?|^club.*?years?'),),
        'Clubs': (_re_compile(r'clubs?'),),
        'Caps(Goals)': (_re_compile(r'caps\(goals\)'),),
        'Caps': (_re_compile(r'caps?'),),
        'Goals': (_re_compile(r'goals?'),),
        'National Years': (_re_compile(r'national.*?years?'),),
        'National Team': (_re_compile(r'national.*?teams?'),),
        'National Caps(Goals)': (_re_compile(r'national.*?caps\(goals\)'),),
        'Youth Clubs': (_re_compile(r'youth.*?clubs?'),),
        'Youth Years': (_re_compile(r'youth.*?years?'),),
        'Youth Caps(Goals)': (_re_compile(r'youth.*?caps\(goals\)'),),
        'Youth Caps': (_re_compile(r'youth.*?caps?'),),
        'Youth Goals': (_re_compile(r'youth[-_\s]*goals?'),),
        'National Caps': (_re_compile(r'national.*?caps?'),),
        'National Goals': (_re_compile(r'national[-_\s]*goals?'),),
        'Total Caps': (_re_compile(r'total.*?caps?'),),
        'Total Goals': (_re_compile(r'total.*?goals?'),),
        'Manager Clubs': (_re_compile(r'manager.*?clubs?'),),
        'Manager Years': (_re_compile(r'manager.*?years?'),),
        'School': (['school'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateFootballOfficial(TemplateBase):
    template_name = 'Football Official'
    fields_map = {
        'League': (_re_compile(r'league'),),
        'Role': (_re_compile(r'roles?'),),
        'International Years': (_re_compile(r'international.*?years'),),
        'Confederation': (_re_compile(r'confederation'),),
        'International Role': (_re_compile(r'international.*?roles?'),)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateAdultBiography(TemplateBase):
    template_name = 'Adult Biography'
    fields_map = {
        'Number Films': (_re_compile(r'number.*?of.*?films'),),
        'Hair Color': (['haircolour'], _re_compile(r'hair.*?color')),
        'Eye Color': (['eyecolour'], _re_compile(r'eye.*?color')),
        'Orientation': (['orientation'],),
        'Measurements': (['measurements'],),
        'Films': (['films', 'film'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateActor(TemplateBase):
    template_name = 'Actor'
    fields_map = {
        'Medium': (['medium'],),
        'Instagram': (['instagram'],),
        'Voice Type': (_re_compile(r'voice.*?type'),),
        'Traditional Chinese Name': (['tradchinesename'],),
        'Simplified Chinese Name': (['simpchinesename'],),
        'Chinese Name': (_re_compile(r'chinese.*?name'),),
        'Pinyin Chines Name': (['pinyinchinesename'],),
        'Agent': (['agent'],),
        'Notable Work': (_re_compile(r'notable.*?works?'),),
        'Instrument': (['instrument'],),
        'Television': (['television'],),
        'Profession': (['profession'],),
        'Notable Role': (['credits'], _re_compile(r'notable.*?roles?'),),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateWarDetainee(TemplateBase):
    template_name = 'War Detainee'
    fields_map = {
        'Arrest Place': (_re_compile(r'arrest.*?place|^place.*?arrest'),),
        'Arrest Date': (_re_compile(r'arrest.*?date|^date.*?arrest'),),
        'Arresting Authority': (_re_compile(r'arresting.*?authority'),),
        'Detained At': (_re_compile(r'detained.*?at'),),
        'Charge': (['charge'],),
        'Id Number': (_re_compile(r'id.*?number'),),
        'Status': (['status'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateVicePresident(TemplateBase):
    template_name = 'Vice President'
    fields_map = {
        'Term Start': (_re_compile(r'term.*?start'),),
        'Term End': (_re_compile(r'term.*?end'),),
        'Successor': (_re_compile(r'successor|^succeeded|^succeeding'),),
        'President': (_re_compile(r'president'),),
        'Profession': (['profession'],),
        'Predecessor': (_re_compile(r'predecessor'),)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateSwimmer(TemplateBase):
    template_name = 'Swimmer'
    fields_map = {
        'Medal': (_re_compile(r'medal.*?templates?'),),
        'National Team': (_re_compile(r'national.*?teams?'),),
        'Coach': (['coach'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateIndonesiaArtist(TemplateBase):
    template_name = 'Indonesia Artist'
    fields_map = {
        'Instrument': (['instrument', 'instruments'],),
        'Influenced': (['influenced', 'influences'],),
        'Record Company': (['label'],),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplatePrimeMinister(TemplateBase):
    template_name = 'Prime Minister'
    fields_map = {
        'Office': (_re_compile(r'office'),),
        'Deputy': (_re_compile(r'deputy'),),
        'Term Start': (_re_compile(r'term.*?start'),),
        'Term End': (_re_compile(r'term.*?end'),),
        'Predecessor': (_re_compile(r'predecessor'),),
        'Successor': (_re_compile(r'successor|^succeeded|^succeeding'),),
        'Prime Minister': (_re_compile(r'prime.*?minister'),),
        'President': (_re_compile(r'president'),),
        'Profession': (['profession'],),
        'Governor': (_re_compile(r'governor|^governor.*?general'),),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateMP(TemplateBase):
    template_name = 'Member of Parliament'
    fields_map = {
        'Office': (_re_compile(r'office'),),
        'Deputy': (_re_compile(r'deputy'),),
        'Term Start': (_re_compile(r'term.*?start'),),
        'Term End': (_re_compile(r'term.*?end'),),
        'Predecessor': (_re_compile(r'predecessor'),),
        'Successor': (_re_compile(r'successor|^succeeded|^succeeding'),),
        'Prime Minister': (_re_compile(r'prime.*?minister'),),
        'Pronunciation': (['pronunciation'],),
        'Profession': (['profession'],),
        'Minister': (_re_compile(r'minister'),),
        'President': (_re_compile(r'president'),),
    }
    fields_map.update(TemplateBase.fields_map)


_TEMPLATE_MAP = {
    TemplateMotorcycleRider: ['infobox motorcycle rider'],
    TemplateEngineer: ['infobox engineer'],
    TemplateChineseActorSinger: ['infobox chinese actor and singer',
                                 'infobox chinese-language singer and actor'],
    TemplateRoyalty: ['infobox royalty', 'infobox diraja'],
    TemplateModel: ['infobox model'],
    TemplateMinister: ['infobox minister'],
    TemplateOfficeholder: ['infobox officeholder'],
    TemplateFootballPlayer: ['infobox football biography', 'pemain bola infobox', 'football player infobox',
                             'infobox football biography 2'],
    TemplateFootballOfficial: ['infobox football official'],
    TemplateAdultBiography: ['infobox adult male', 'infobox adult biography'],
    TemplateActor: ['infobox actor', 'infobox actor voice'],
    TemplateWarDetainee: ['infobox war on terror detainee', 'infobox wot detainees'],
    TemplateVicePresident: ['infobox vice president'],
    TemplateSwimmer: ['infobox swimmer'],
    TemplateIndonesiaArtist: ['infobox artis indonesia'],
    TemplatePrimeMinister: ['infobox_prime minister', 'infobox prime minister'],
    TemplateMP: ['infobox mp']
}

TEMPLATE_MAP = {i: k for k, v in _TEMPLATE_MAP.items() for i in v}

if __name__ == '__main__':
    value = {
        "subject_name": "Omar Ahmed Khadr",
        "image_name": "Omar Khadr - PD-Family-released.jpg",
        "image_size": "250px",
        "image_caption": "Khadr semasa berumur 14 tahun",
        "date_of_birth": "{{Birth date and age|1986|9|19}}",
        "place_of_birth": "Toronto, Kanada",
        "detained_at": "Guantanamo",
        "id_number": "766",
        "status": "Tribunal underway",
        "parents": "[[Ahmed Said Khadr]]<br />[[Maha Elsamnah]]"
    }
    tem = TemplateWarDetainee(value, 'Omar Ahmed Khadr')
    print(tem.fields)
