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

_FILE_LOG_LEVEL = logging.ERROR
_CONSOLE_LOG_LEVEL = logging.ERROR

_file_log = LoggerUtil('src.templates.file', file_path='../log/templates.log',
                       level=_FILE_LOG_LEVEL, mode='w+')
_console_log = LoggerUtil('src.templates.console', level=_CONSOLE_LOG_LEVEL)


def _is_int(ind):
    try:
        int(ind)
        return True
    except ValueError:
        return False


def _is_include_dict(array):
    for i in array:
        if isinstance(i, dict):
            return True
    return False


def _get_key(array, mode='max'):
    assert mode in ['min', 'max'], f'不支持的mode{mode}'
    m_k = None
    if mode == 'min':
        m_v = float('inf')
        for i in array:
            for k, v in i.items():
                if len(v) < m_v:
                    m_k = [j for i in v for j in i.keys()]
                    m_v = len(v)
    else:
        m_v = -float('inf')
        for i in array:
            for k, v in i.items():
                if len(v) > m_v:
                    m_k = [j for i in v for j in i.keys()]
                    m_v = len(v)
    return m_k


def _get_multi_values(array, force=False):
    mode = 'max' if not force else 'min'
    ky = _get_key(array, mode)
    ky = {k: [] for k in ky}
    for i in array:
        for k, v in i.items():
            for ii in v:
                for kk, vv in ii.items():
                    try:
                        ky[kk].append(k.lower() + ':' + vv)
                    except KeyError:
                        pass
    result = []
    for i in ky.values():
        result.append('\n'.join(i))
    return result


def _re_compile(s, mode='se'):
    assert mode in ['s', 'e', 'se'], f'不支持{mode}'
    _s = r'^'
    _e = r'\s*(?P<e_index{}>\d*)$'
    if mode == 's':
        _p = _s + '{}'
    elif mode == 'e':
        _p = '{}' + _e
    else:
        _p = _s + '{}' + _e
    s = s.split('|')
    s = [r'\D*?(?P<i_index{}>\d*)\D*?'.join(i.split('.*?')).format(*list(range(j, len(i.split('.*?')) + j)))
         for j, i in enumerate(s)]
    s = '|'.join([_p.format(i, j) for j, i in enumerate(s)])
    return re.compile(r'%s' % s)


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


TEST = {'test': []}


class TemplateBase:
    template_name = 'Base'
    multi_len = 0
    fields_map = {
        'Name': ({'zh': '名字'}, ['name', 'nama'],),
        'Alias': ({'zh': '别名'}, ['alias', 'nickname'], _re_compile(r'other.*?names?')),
        'Native Name': ({'zh': '本地名字'}, _re_compile(r'native.*?names?'),),
        'Birth': ({'zh': '出生信息'}, ['birth', 'born'],),
        'Birth Name': ({'zh': '出生名'}, _re_compile(r'birth.*?names?'),),
        'Birth Date': ({'zh': '出生日期'}, _re_compile(r'birth.*?date|date.*?birth'),),
        'Birth Place': ({'zh': '出生地点'}, ['tempat lahir'], _re_compile(r'birth.*?place|place.*?birth')),
        'Retirement Date': ({'zh': '退休时间'}, ['retired']),
        'Birth City': ({'zh': '出生城市'}, _re_compile(r'birth.*?city|city.*?birth'),),
        'Birth Country': ({'zh': '出生国家'}, _re_compile(r'birth.*?country|country.*?birth'),),
        'Height': ({'zh': '身高'}, ['height'],),
        'Weight': ({'zh': '体重'}, ['weight'],),
        'Nationality': ({'zh': '国籍'}, ['nationality'],),
        'Website': ({'zh': '网站'}, ['website', 'url', 'homepage'],),
        'Origin': ({'zh': '源自'}, ['origin'],),
        'Religion': ({'zh': '宗教'}, ['religion', 'agama'],),
        'Education': ({'zh': '教育'}, ['education', 'pendidikan'],),
        'Occupation': ({'zh': '职业'}, ['occupation', 'occupation(s)', 'pekerjaan', 'ocupation', 'occuption',
                                      'occuoation', 'profession'],),
        'Years Active': ({'zh': '活跃年份'}, ['active', 'yeaesactive'], _re_compile(r'year.*?active')),
        'Death Date': ({'zh': '死亡日期'}, _re_compile(r'death.*?date|date.*?death'),),
        'Death Place': ({'zh': '死亡时间'}, _re_compile(r'death.*?place|place.*?death'),),
        'Burial Place': ({'zh': '埋葬地点'}, _re_compile(r'resting.*?place|burial.*?place'),),
        'Spouse': ({'zh': '伴侣'}, ['spouse', 'pasangan', 'spouses'],),
        'Parents': ({'zh': '父母'}, ['parents'],),
        'Children': ({'zh': '孩子'}, ['children', 'issue'],),
        'Gender': ({'zh': '性别'}, ['gender'],),
        'Alma Mater': ({'zh': '母校'}, _re_compile(r'alma.*?mater'),),
        'Location': ({'zh': '地点'}, ['location'],),
        'Relatives': ({'zh': '关系'}, _re_compile(r'relatives?|relations?'),),
        'Full Name': ({'zh': '全名'}, _re_compile(r'full.*?name'),),
        'Father': ({'zh': '父亲'}, ['father', 'bapa'],),
        'Mother': ({'zh': '目前'}, ['mother'],),
        'Residence': ({'zh': '住宅'}, ['residence', 'house', 'residential', 'royal house', 'palace'],),
        'Known For': ({'zh': '著名'}, ['known'], _re_compile(r'known.*?for'),),
        'Partner': ({'zh': '伙伴'}, ['partner'],),
        'Citizenship': ({'zh': '市民'}, ['citizenship'],),
        'Honorific Prefix': ({'zh': '尊称前缀'}, _re_compile(r'honorific.*?prefix'),),
        'Honorific Suffix': ({'zh': '尊称后缀'}, _re_compile(r'honorific.*?suffix'),),
        'Home Town': ({'zh': '家乡'}, _re_compile(r'home.*?town'),),
        'Employer': ({'zh': '雇主'}, ['employer'],),
        'Leader': ({'zh': '领导'}, _re_compile(r'leader'),),
        'Family': ({'zh': '家庭'}, ['family'],),
        'Ethnicity': ({'zh': '种族'}, ['ethnicity', 'ethnic'],),
        'Subject': ({'zh': '学科'}, ['subject', 'discipline'],),
        'Works': ({'zh': '作品'}, ['works', 'associated_acts', 'associated acts', 'associatedacts', 'associated-acts'],
                  _re_compile(r'notable.*?works?')),
        'Net Worth': ({'zh': '净值'}, _re_compile(r'net.*?worth'),),
        'Awards': ({'zh': '奖项'}, ['prizes'], _re_compile(r'awards?', mode='e'),),
        'Projects': ({'zh': '项目'}, _re_compile(r'projects?', mode='e'),),
        'Institutions': ({'zh': '机构'}, ['agency'], _re_compile(r'institutions?|work.*?institutions?')),
        'School': ({'zh': '学校'}, ['school', 'college'],),
        'Hair Color': ({'zh': '发色'}, ['haircolour'], _re_compile(r'hair.*?color')),
        'Eye Color': ({'zh': '眼睛颜色'}, ['eyecolour'], _re_compile(r'eye.*?color')),
        'Measurements': ({'zh': '三围'}, ['measurements'],),
    }
    multi_values_field = None

    _dont_parse = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading]

    def __init__(self, values, entry, force=False, multi_dict=None):
        self._fields = {'template_name': self.template_name,
                        'fields': {k: {'props': v[0], 'values': []} if isinstance(v[0], dict) else {'values': []} for
                                   k, v in self.fields_map.items()},
                        'entry': entry}
        for k, v in values.items():
            field = None
            index = None
            for kk, vv in self.fields_map.items():
                assert isinstance(vv, tuple), f'fields map中的value为不支持的类型: {type(vv)}'
                if len(vv) == 2 or len(vv) == 1:
                    try:
                        vvv = vv[1]
                    except IndexError:
                        vvv = vv[0]
                    if isinstance(vvv, list):
                        if k.lower().strip() in vvv:
                            field = kk
                            break
                    elif isinstance(vvv, re.Pattern):
                        res = re.search(vvv, k.lower().strip())
                        if res:
                            if any(res.groups()):
                                for i in res.groups():
                                    try:
                                        index = int(i)
                                        break
                                    except (TypeError, ValueError):
                                        continue
                            field = kk
                            break
                    else:
                        raise TypeError(f'fields map中的value为不支持的类型: {type(vvv)}')
                elif len(vv) == 3:
                    v_l = vv[1]
                    v_r = vv[2]
                    assert isinstance(v_l, list) and isinstance(v_r,
                                                                re.Pattern), f'列表中的第一个为list枚举类型，第二个为正则表达式类型，目前的类型为: {type(v_l)}, {type(v_r)}'
                    if k.lower().strip() in v_l:
                        field = kk
                        break
                    else:
                        res = re.search(v_r, k.lower().strip())
                        if res:
                            field = kk
                            if any(res.groups()):
                                for i in res.groups():
                                    try:
                                        index = int(i)
                                        break
                                    except (TypeError, ValueError):
                                        continue
                            break
                else:
                    raise ValueError('不支持的fields map类型')
            if field:
                p_v = self.parse(v.strip())
                h_v = ''.join([str(i) for i in p_v]).strip()
                if h_v:
                    _console_log.logger.debug(f'\n{field}: {h_v}\n')
                    if index:
                        h_v = {index: h_v}
                    self._fields['fields'][field]['values'].append(h_v)
        if self.multi_values_field is not None:
            fields_values = {k: v for k, v in self._fields['fields'].items() if
                             v['values'] and all([k not in kk[1] if len(kk) > 1 else k not in kk[0] for kk in
                                                  self.multi_values_field.values()])}
            multi_values_field = {k: {'props': v[0], 'values': []} if isinstance(v[0], dict) else {'values': []} for
                                  k, v in self.multi_values_field.items()}
            for k, v in self._fields['fields'].items():
                if v['values']:
                    for i_k, i_v in self.multi_values_field.items():
                        if len(i_v) > 1:
                            i_f = i_v[1]
                        else:
                            i_f = i_v[0]
                        if k in i_f:
                            for iii, jjj in enumerate(v['values']):
                                if not isinstance(jjj, dict):
                                    v['values'][iii] = {0: v['values'][iii]}
                                    break
                            multi_values_field[i_k]['values'].append({k: v['values']})
            for v in multi_values_field.values():
                if v['values']:
                    v['values'] = _get_multi_values(v['values'], force=force)
            multi_values_field = {k: v for k, v in multi_values_field.items() if v['values']}
            fields_values.update(multi_values_field)
        else:
            fields_values = {}
            multi_values_field = []
            name = []
            for k, v in self._fields['fields'].items():
                if v['values']:
                    if _is_include_dict(v['values']):
                        for iii, jjj in enumerate(v['values']):
                            if not isinstance(jjj, dict):
                                v['values'][iii] = {0: v['values'][iii]}
                                break
                        name.append(k)
                        multi_values_field.append({k: v['values']})
                    else:
                        fields_values[k] = v
            if multi_values_field:
                _console_log.logger.info(name)
                if multi_dict is not None:
                    for jj in name:
                        if jj not in multi_dict[self.template_name]:
                            multi_dict[self.template_name].append(jj)
                fields_values.update({'Other Info': {'props': {'zh': '其他信息'},
                                                     'values': _get_multi_values(multi_values_field, force=force)}})
        self._fields['fields'] = fields_values

    @classmethod
    def parse(cls, p_t):
        p_t = mwp.parse(p_t)
        p_t = p_t.filter(recursive=False)
        for i, j in enumerate(p_t):
            if isinstance(j, mwp.wikicode.Template):
                values = []
                for k in j.params:

                    # if not _is_int(str(k.name)):
                    #     if str(k.name).strip() not in TEST['test']:
                    #         TEST['test'].append(str(k.name).strip())

                    if _is_int(str(k.name)) and str(k.value) not in ['zh-hans']:
                        values.append(str(k.value))
                    elif str(k.name) in ['m', 'end', 'reason', 'award', 'ft', 'in', 'meter', 'meters', 'cm']:
                        values.append(f'({str(k.name)}: {str(k.value)})')
                p_t[i] = mwp.parse('-'.join(values))
            elif isinstance(j, mwp.wikicode.ExternalLink):
                p_t[i] = j.url
            elif isinstance(j, mwp.wikicode.Tag):
                rs = mwp.parse('\n') if str(j.tag) == 'br' else j.contents
                p_t[i] = rs
            elif isinstance(j, mwp.wikicode.Wikilink):
                p_t[i] = j.text if j.text else j.title
            elif isinstance(j, mwp.wikicode.HTMLEntity):
                p_t[i] = mwp.parse(j.normalize())
            elif any([isinstance(j, k) for k in cls._dont_parse]):
                p_t[i] = mwp.parse(None)
        if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
            return p_t
        return cls.parse(p_t)

    @property
    def fields(self):
        return self._fields

    @property
    def graph_entities(self):
        result = []
        fields = self.fields
        t_n = fields['template_name']
        s_e = fields['entry']
        for k, v in fields['fields'].items():
            attr = v.get('props', {})
            for vl in v['values']:
                result.append((k, vl, attr))
        return {'node_label': t_n, 'node_name': s_e, 'node_relation': result}


class TemplateMotorcycleRider(TemplateBase):
    template_name = 'Motorcycle Rider'
    fields_map = {
        'Current Team': ({'zh': '目前团队'}, _re_compile(r'current.*?team'),),
        'Bike Number': ({'zh': '自行车号码'}, _re_compile(r'bike.*?number'),)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateEngineer(TemplateBase):
    template_name = 'Engineer'


class TemplateChineseActorSinger(TemplateBase):
    template_name = 'Chinese Actor And Singer'
    fields_map = {
        'Traditional Chinese Name': ({'zh': '繁体名字'}, ['tradchinesename'],),
        'Pinyin Chines Name': ({'zh': '名字拼音'}, ['pinyinchinesename'],),
        'Simplified Chinese Name': ({'zh': '简体名字'}, ['simpchinesename'],),
        'Genre': ({'zh': '类型'}, ['genre'],),
        'Record Company': ({'zh': '唱片公司'}, ['label'],),
        'Instrument': ({'zh': '乐器'}, ['instrument', 'instruments'],),
        'Influenced': ({'zh': '影响'}, ['influenced', 'influences'],),
        'Voice Type': ({'zh': '声音类型'}, _re_compile(r'voice.*?type'),),
        'Chinese Name': ({'zh': '中文名'}, _re_compile(r'chinese.*?name'),),
        'Notable Role': ({'zh': '著名角色'}, _re_compile(r'notable.*?roles?'),),
        'Associated Artists': (
            {'zh': '相关艺术家'}, ['associatedact', 'associated act', 'associated_act', 'associated-act'],),
        'Current Members': ({'zh': '现有成员'}, _re_compile(r'current.*?members?'),),
        'Past Members': ({'zh': '过去成员'}, _re_compile(r'past.*?members?'),),
        'English Name': ({'zh': '英文名'}, _re_compile(r'nama.*?inggeris'),)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateRoyalty(TemplateBase):
    template_name = 'Royalty'
    fields_map = {
        'Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor')),
        'Reign': ({'zh': '在位'}, _re_compile(r'reign'),),
        'Coronation': ({'zh': '加冕礼'}, _re_compile(r'coronation'),),
        'Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor'),),
        'Succession': ({'zh': '继承'}, _re_compile(r'succession'),),
        'Regent': ({'zh': '摄政'}, _re_compile(r'regent'),)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Office': ({'zh': '任职信息'}, ['Successor', 'Reign', 'Coronation', 'Predecessor', 'Succession', 'Regent']),
        'Native Name': ({'zh': '本地名字'}, ['Native Name'])}


class TemplateModel(TemplateBase):
    template_name = 'Model'
    fields_map = {
        'Dress Size': ({'zh': '服装尺码'}, _re_compile(r'dress.*?size'),),
        'Shoe Size': ({'zh': '鞋子尺码'}, _re_compile(r'shoe.*?size'),),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateMinister(TemplateBase):
    template_name = 'Minister'
    fields_map = {
        'Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        'Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        'Party': ({'zh': '政党'}, ['party'],),
        'Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        'Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor'),)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'}, ['Office', 'Prime Minister', 'Term Start', 'Predecessor'])}


class TemplateOfficeholder(TemplateBase):
    template_name = 'Officeholder'
    fields_map = {
        'Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        'Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        'Majority': ({'zh': '多数'}, _re_compile(r'majority')),
        'Assembly': ({'zh': '议会'}, _re_compile(r'assembly')),
        'State': ({'zh': '州'}, ['state']),
        'Deputy': ({'zh': '副职'}, _re_compile(r'deputy'),),
        'Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        'Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        'Term': ({'zh': '在位时间'}, _re_compile(r'term'),),
        'Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor'),),
        'Successor': ({'zh': '后任'}, _re_compile(r'successor|succeeded|succeeding'),),
        'Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        'Pronunciation': ({'zh': '发音'}, ['pronunciation'],),
        'Alongside': ({'zh': '合作'}, _re_compile(r'alongside'),),
        'President': ({'zh': '总统'}, _re_compile(r'president'),),
        'Governor': ({'zh': '总督'}, _re_compile(r'governor|governor.*?general'),),
        'Vice President': ({'zh': '副总统'}, _re_compile(r'vice.*?president'),),
        'Branch': ({'zh': '兵役分支'}, ['branch'],),
        'Service Years': ({'zh': '兵役时间'}, _re_compile(r'service.*?years?'),),
        'Appointer': ({'zh': '任命者'}, _re_compile(r'appointer'),),
        'Minister': ({'zh': '部长'}, _re_compile(r'minister'),),
        'Cabinet': ({'zh': '内阁'}, ['cabinet'],),
        'Department': ({'zh': '部门'}, ['department'],),
        'Nominator': ({'zh': '提名人'}, _re_compile(r'nominator'),),
        'Chancellor': ({'zh': '校长'}, _re_compile(r'chancellor'),),
        'Lieutenant': ({'zh': '中尉'}, _re_compile(r'lieutenant'),),
        'Appointed': ({'zh': '任职日期'}, _re_compile(r'appointed'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['Office', 'Deputy', 'Term Start', 'Term End', 'Predecessor', 'Successor',
                                      'Prime Minister', 'President', 'Governor', 'Alongside', 'Minister', 'Appointer',
                                      'Term', 'Chancellor', 'Leader', 'Lieutenant', 'Vice President', 'Nominator',
                                      'Appointed', 'Monarch', 'Majority', 'Assembly', 'State'])}


class TemplateFootballPlayer(TemplateBase):
    template_name = 'Football Player'
    fields_map = {
        'Player Name': ({'zh': '运动员名称'}, _re_compile(r'player.*?name'),),
        'Current Club': ({'zh': '目前俱乐部'}, _re_compile(r'current.*?club'),),
        'Club Number': ({'zh': '运动员编号'}, _re_compile(r'club.*?number'),),
        'Position': ({'zh': '运动员定位'}, ['position'],),
        'Years': ({'zh': '服役年份'}, _re_compile(r'years?|club.*?years?'),),
        'Clubs': ({'zh': '服役俱乐部'}, _re_compile(r'clubs?'),),
        'Caps(Goals)': ({'zh': '出场数(进球数)'}, _re_compile(r'caps\(goals\)'),),
        'Caps': ({'zh': '出场数'}, _re_compile(r'caps?'),),
        'Goals': ({'zh': '进球数'}, _re_compile(r'goals?'),),
        'National Years': ({'zh': '国家队服役年份'}, _re_compile(r'national.*?years?'),),
        'National Team': ({'zh': '国家队'}, _re_compile(r'national.*?teams?'),),
        'National Caps(Goals)': ({'zh': '在国家队出场数(在国家队进球数)'}, _re_compile(r'national.*?caps\(goals\)'),),
        'Youth Clubs': ({'zh': '青年俱乐部'}, _re_compile(r'youth.*?clubs?'),),
        'Youth Years': ({'zh': '青年俱乐部服役年份'}, _re_compile(r'youth.*?years?'),),
        'Youth Caps(Goals)': ({'zh': '在青年俱乐部出场数(在青年俱乐部进球数)'}, _re_compile(r'youth.*?caps\(goals\)'),),
        'Youth Caps': ({'zh': '在青年俱乐部出场数'}, _re_compile(r'youth.*?caps?'),),
        'Youth Goals': ({'zh': '在青年俱乐部进球数'}, _re_compile(r'youth[-_\s]*goals?'),),
        'National Caps': ({'zh': '在国家队出场数'}, _re_compile(r'national.*?caps?'),),
        'National Goals': ({'zh': '在国家队进球数'}, _re_compile(r'national[-_\s]*goals?'),),
        'Total Caps': ({'zh': '总出场数'}, _re_compile(r'total.*?caps?'),),
        'Total Goals': ({'zh': '总进球数'}, _re_compile(r'total.*?goals?'),),
        'Manager Clubs': ({'zh': '管理俱乐部'}, _re_compile(r'manager.*?clubs?'),),
        'Manager Years': ({'zh': '管理俱乐部年份'}, _re_compile(r'manager.*?years?'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Clubs': ({'zh': '服役俱乐部'}, ['Years', 'Clubs', 'Caps', 'Goals', 'Caps(Goals)']),
                          'National Team': (
                              {'zh': '服役国家队'}, ['National Years', 'National Team', 'National Caps', 'National Goals',
                                                'National Caps(Goals)']),
                          'Youth Clubs': ({'zh': '服役青年俱乐部'},
                                          ['Youth Clubs', 'Youth Years', 'Youth Caps(Goals)', 'Youth Caps',
                                           'Youth Goals']),
                          'Manager Clubs': ({'zh': '管理俱乐部'}, ['Manager Clubs', 'Manager Years'])}


class TemplateFootballOfficial(TemplateBase):
    template_name = 'Football Official'
    fields_map = {
        'League': ({'zh': '联盟'}, _re_compile(r'league'),),
        'Role': ({'zh': '角色'}, _re_compile(r'roles?'),),
        'International Years': ({'zh': '国际年份'}, _re_compile(r'international.*?years'),),
        'International League': ({'zh': '国际联盟'}, _re_compile(r'confederation'),),
        'International Role': ({'zh': '国际角色'}, _re_compile(r'international.*?roles?'),)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['League', 'Role', 'International Years', 'Confederation', 'International Role'])}


class TemplateAdultBiography(TemplateBase):
    template_name = 'Adult Biography'
    fields_map = {
        'Number Films': ({'zh': '电影数目'}, _re_compile(r'number.*?of.*?films'),),
        'Orientation': ({'zh': '性取向'}, ['orientation'],),
        'Films': ({'zh': '电影'}, ['films', 'film'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateActor(TemplateBase):
    template_name = 'Actor'
    fields_map = {
        'Voice Type': ({'zh': '声音类型'}, _re_compile(r'voice.*?type'),),
        'Traditional Chinese Name': ({'zh': '繁体名字'}, ['tradchinesename'],),
        'Simplified Chinese Name': ({'zh': '简体名字'}, ['simpchinesename'],),
        'Chinese Name': ({'zh': '中文名'}, _re_compile(r'chinese.*?name'),),
        'Pinyin Chines Name': ({'zh': '名字拼音'}, ['pinyinchinesename'],),
        'Agent': ({'zh': '经纪人'}, ['agent'],),
        'Instrument': ({'zh': '乐器'}, ['instrument'],),
        'Television': ({'zh': '电视节目'}, ['television'],),
        'Notable Role': ({'zh': '著名角色'}, ['credits'], _re_compile(r'notable.*?roles?'),),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateWarDetainee(TemplateBase):
    template_name = 'War Detainee'
    fields_map = {
        'Arrest Place': ({'zh': '逮捕地点'}, _re_compile(r'arrest.*?place|place.*?arrest'),),
        'Arrest Date': ({'zh': '逮捕日期'}, _re_compile(r'arrest.*?date|date.*?arrest'),),
        'Arresting Authority': ({'zh': '逮捕机关'}, _re_compile(r'arresting.*?authority'),),
        'Detained At': ({'zh': '拘留处'}, _re_compile(r'detained.*?at'),),
        'Charge': ({'zh': '指控'}, ['charge'],),
        'Status': ({'zh': '状态'}, ['status'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateVicePresident(TemplateBase):
    template_name = 'Vice President'
    fields_map = {
        'Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        'Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        'Successor': ({'zh': '后任'}, _re_compile(r'successor|succeeded|succeeding'),),
        'President': ({'zh': '总统'}, _re_compile(r'president'),),
        'Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor'),)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['Term Start', 'Term End', 'Successor', 'President', 'Predecessor'])}


class TemplateSwimmer(TemplateBase):
    template_name = 'Swimmer'
    fields_map = {
        'Medal': ({'zh': '奖牌'}, _re_compile(r'medal.*?templates?'),),
        'National Team': ({'zh': '国家队'}, _re_compile(r'national.*?teams?'),),
        'Coach': ({'zh': '教练'}, ['coach'],)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateIndonesiaArtist(TemplateBase):
    template_name = 'Indonesia Artist'
    fields_map = {
        'Instrument': ({'zh': '乐器'}, ['instrument', 'instruments'],),
        'Influenced': ({'zh': '影响'}, ['influenced', 'influences'],),
        'Record Company': ({'zh': '唱片公司'}, ['label'],),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplatePrimeMinister(TemplateBase):
    template_name = 'Prime Minister'
    fields_map = {
        'Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        'Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        'Deputy': ({'zh': '副职'}, _re_compile(r'deputy'),),
        'Assembly': ({'zh': '议会'}, _re_compile(r'assembly')),
        'Majority': ({'zh': '多数'}, _re_compile(r'majority')),
        'Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        'Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        'Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor'),),
        'Successor': ({'zh': '后任'}, _re_compile(r'successor|succeeded|succeeding'),),
        'Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        'President': ({'zh': '总统'}, _re_compile(r'president'),),
        'Governor': ({'zh': '总督'}, _re_compile(r'governor|governor.*?general'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['Deputy', 'Term Start', 'Term End', 'Predecessor', 'Successor', 'President',
                                      'Prime Minister', 'Office', 'Leader', 'Monarch', 'Majority', 'Assembly'])}


class TemplateMP(TemplateBase):
    template_name = 'Member of Parliament'
    fields_map = {
        'Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        'Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        'Majority': ({'zh': '多数'}, _re_compile(r'majority')),
        'Deputy': ({'zh': '副职'}, _re_compile(r'deputy'),),
        'Assembly': ({'zh': '议会'}, _re_compile(r'assembly')),
        'Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        'Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        'Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor'),),
        'Successor': ({'zh': '后任'}, _re_compile(r'successor|succeeded|succeeding'),),
        'Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        'Pronunciation': ({'zh': '发音'}, ['pronunciation'],),
        'Minister': ({'zh': '部长'}, _re_compile(r'minister'),),
        'President': ({'zh': '总统'}, _re_compile(r'president'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['Office', 'Term Start', 'Term End', 'Predecessor', 'Successor', 'Minister',
                                      'Deputy', 'Prime Minister', 'President', 'Monarch', 'Majority', 'Assembly'])}


class TemplateScientist(TemplateBase):
    template_name = 'Scientist'
    fields_map = {
        'Workplace': ({'zh': '工作地'}, _re_compile(r'work.*?places?')),
        'Thesis Year': ({'zh': '论文年份'}, _re_compile(r'thesis.*?years?')),
        'Thesis Title': ({'zh': '论文标题'}, _re_compile(r'thesis.*?titles?')),
        'Thesis Url': ({'zh': '论文链接'}, _re_compile(r'thesis.*?urls?')),
        'Fields': ({'zh': '领域'}, ['field', 'fields']),
        'Academic Advisors': ({'zh': '学术顾问'}, _re_compile(r'academic.*?advisors?')),
        'Doctoral Advisors': ({'zh': '博士生导师'}, _re_compile(r'doctoral.*?advisors?')),
        'Influenced': ({'zh': '影响'}, ['influenced', 'influences'],),
        'Boards': ({'zh': '董事会'}, ['boards']),
        'Doctoral Students': ({'zh': '博士生'}, _re_compile(r'doctoral.*?students?')),
        'Notable Students': ({'zh': '著名学生'}, _re_compile(r'notable.*?students?'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateEconomist(TemplateBase):
    template_name = 'Economist'
    fields_map = {
        'Fields': ({'zh': '领域'}, ['field', 'fields']),
        'Contributions': ({'zh': '贡献'}, ['contributions', 'contribution']),
        'Influenced': ({'zh': '影响'}, ['influenced', 'influences'],),
        'Doctoral Students': ({'zh': '博士生'}, _re_compile(r'doctoral.*?students?')),
        'Doctoral Advisors': ({'zh': '博士生导师'}, _re_compile(r'doctoral.*?advisors?')),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateGovernor(TemplateBase):
    template_name = 'Governor'
    fields_map = {
        'Deputy': ({'zh': '副职'}, _re_compile(r'deputy'),),
        'Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        'Lieutenant': ({'zh': '中尉'}, _re_compile(r'lieutenant'),),
        'Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor')),
        'Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        'Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        'Vice Governor': ({'zh': '副总督'}, _re_compile(r'vice.*?governor')),
        'Party': ({'zh': '政党'}, ['party'],),
        'Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        'Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor'),),
        'President': ({'zh': '总统'}, _re_compile(r'president'),),
        'Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateSenator(TemplateBase):
    template_name = 'Senator'
    fields_map = {
        'State': ({'zh': '州'}, ['state']),
        'Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        'Successor': ({'zh': '后任'}, _re_compile(r'successor|succeeded|succeeding'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'}, ['State', 'Term Start', 'Successor'])}


class TemplateGolfer(TemplateBase):
    template_name = 'Golfer'
    fields_map = {
        'Years': ({'zh': '获奖年份'}, _re_compile(r'years?'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Awards': ({'zh': '奖项'}, ['Awards', 'Years'])
    }


class TemplateFieldHockeyPlayer(TemplateBase):
    template_name = 'Field Hockey Player'
    fields_map = {
        'Position': ({'zh': '运动员定位'}, ['position'],),
        'Years': ({'zh': '服役年份'}, _re_compile(r'years?|club.*?years?'),),
        'Clubs': ({'zh': '服役俱乐部'}, _re_compile(r'clubs?'),),
        'Caps': ({'zh': '出场数'}, _re_compile(r'caps?'),),
        'Goals': ({'zh': '进球数'}, _re_compile(r'goals?'),),
        'National Years': ({'zh': '国家队服役年份'}, _re_compile(r'national.*?years?'),),
        'National Team': ({'zh': '国家队'}, _re_compile(r'national.*?teams?'),),
        'National Caps': ({'zh': '在国家队出场数'}, _re_compile(r'national.*?caps?'),),
        'National Goals': ({'zh': '在国家队进球数'}, _re_compile(r'national[-_\s]*goals?'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Clubs': ({'zh': '服役俱乐部'}, ['Years', 'Clubs', 'Caps', 'Goals']),
                          'National Team': (
                              {'zh': '服役国家队'}, ['National Years', 'National Team', 'National Caps', 'National Goals'])}


class TemplateTennisPlayer(TemplateBase):
    """ Victoria Azarenka """
    template_name = 'Tennis Player'
    fields_map = {
        'Competition': ({'zh': '比赛'}, _re_compile(r'result', mode='e')),
        'Coach': ({'zh': '教练'}, ['coach']),
        'Current Doubles Ranking': ({'zh': '目前双打排名'}, _re_compile(r'current.*?double.*?ranking'))
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
    TemplateOfficeholder: ['infobox officeholder', 'infobox_officeholder'],
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
    TemplateMP: ['infobox mp'],
    TemplateScientist: ['infobox ahli sains', 'infobox_scientist', 'infobox scientist'],
    TemplateEconomist: ['infobox economist'],
    TemplateGovernor: ['infobox governor general', 'infobox governor'],
    TemplateSenator: ['infobox senator'],
    TemplateGolfer: ['infobox golfer'],
    TemplateFieldHockeyPlayer: ['infobox field hockey player']
}

TEMPLATE_MAP = {i: k for k, v in _TEMPLATE_MAP.items() for i in v}

MULTI_DICT = {i.template_name: [] for i in _TEMPLATE_MAP.keys()}

if __name__ == '__main__':
    value = {
        "name": "Lalit Upadhyay",
        "birth_date": "{{birth date and age|1993|12|1|df=yes}}",
        "birth_place": "[[Varanasi]], [[Uttar Pradesh]], [[India]]<ref>{{cite web|title=Hapless victim of a TV sting, this hockey player is now a rising star|url=http://archive.indianexpress.com/news/hapless-victim-of-a-tv-sting-this-hockey-player-is-now-a-rising-star/938634/|publisher=The Indian Express|accessdate=27 July 2016}}</ref>",
        "position": "Pertahanan",
        "nationalteam1": "{{nfh|India}}",
        "updated": "8 Julai 2016"
    }
    tem = TemplateFieldHockeyPlayer(value, 'Test')
    print(tem.fields)
    # print(tem.graph_entities)
