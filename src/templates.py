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

_FILE_LOG_LEVEL = logging.WARNING
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


def _get_key(array):
    keys = []
    for i in array:
        for v in i.values():
            for k in v:
                e = list(k.keys())[0]
                if e not in keys:
                    keys.append(e)
    return keys


def _get_multi_values(array):
    ky = _get_key(array)
    ky = {k: [] for k in ky}
    for i in array:
        for k, v in i.items():
            for ii in v:
                kk = list(ii.keys())[0]
                vv = ii[kk]
                ky[kk].append(k.lower().split('_')[-1] + ':' + vv)
    result = []
    for i in ky.values():
        result.append('\n'.join(i))
    return result


def _re_compile(s, mode='se', split='.*?'):
    assert mode in ['s', 'e', 'se'], f'不支持{mode}'
    _s = r'^'
    _e = r'$'
    if mode == 's':
        _p = _s + '{}'
    elif mode == 'e':
        _p = '{}' + _e
    else:
        _p = _s + '{}' + _e
    s = s.split('|')
    ss = []
    for j, i in enumerate(s):
        i_split = i.split(split)
        index = []
        for k in range(len(i_split)):
            index.append('i' + str(j))
            index.append(str(j + k))
        ss.append(r'\s*?(?P<s_index{}>\d*)\s*?'.format(j) + r'\D*?(?P<{}_index{}>\d*)\D*?'.join(i_split).format(
            *index) + r'\s*?(?P<e_index{}>\d*)\s*?'.format(j))
    s = ss
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
    fields_map = {
        'Name': ({'zh': '名字'}, ['name', 'nama'],),
        'Alias': ({'zh': '别名'}, ['alias', 'nickname', 'hangul', 'id'], _re_compile(r'other.*?names?|real.*?name')),
        'Native Name': ({'zh': '本地名字'}, _re_compile(r'native.*?names?'),),
        'Birth': ({'zh': '出生信息'}, ['birth', 'born'],),
        'Death': ({'zh': '死亡信息'}, ['died']),
        'Birth Name': ({'zh': '出生名'}, _re_compile(r'birth.*?names?'),),
        'Birth Date': ({'zh': '出生日期'}, _re_compile(r'birth.*?date|date.*?birth'),),
        'Birth Place': ({'zh': '出生地点'}, ['tempat lahir'], _re_compile(r'birth.*?place|place.*?birth')),
        'Retirement Date': ({'zh': '退休时间'}, ['retired'], _re_compile(r'date.*?ret')),
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
                                      'occuoation', 'profession'], _re_compile(r'current.*?occupation')),
        'Years Active': ({'zh': '活跃年份'}, ['active', 'yeaesactive', 'era'], _re_compile(r'year.*?active')),
        'Death Date': ({'zh': '死亡日期'}, _re_compile(r'death.*?date|date.*?death'),),
        'Death Place': ({'zh': '死亡时间'}, _re_compile(r'death.*?place|place.*?death'),),
        'Burial Place': ({'zh': '埋葬地点'}, _re_compile(r'resting.*?place|burial.*?place'),),
        'Spouse': ({'zh': '伴侣'}, ['spouse', 'pasangan', 'spouses'],),
        'Parents': ({'zh': '父母'}, ['parents'],),
        'Sibling': ({'zh': '兄弟姐妹'}, ['sibling']),
        'Children': ({'zh': '孩子'}, ['children', 'issue'],),
        'Gender': ({'zh': '性别'}, ['gender'],),
        'Alma Mater': ({'zh': '母校'}, _re_compile(r'alma.*?mater'),),
        'Relatives': ({'zh': '关系'}, ['relatives,husband'], _re_compile(r'relatives?|relations?'),),
        'Full Name': ({'zh': '全名'}, _re_compile(r'full.*?name'),),
        'Father': ({'zh': '父亲'}, ['father', 'bapa'],),
        'Mother': ({'zh': '目前'}, ['mother'],),
        'Residence': ({'zh': '住宅'}, ['residence', 'residential'],),
        'Known For': ({'zh': '著名'}, ['known'], _re_compile(r'known.*?for'),),
        'Partner': ({'zh': '伙伴'}, ['partner'], _re_compile(r'former.*?partner')),
        'Citizenship': ({'zh': '市民'}, ['citizenship'],),
        'Honorific Prefix': ({'zh': '尊称前缀'}, _re_compile(r'honorific.*?prefix'),),
        'Honorific Suffix': ({'zh': '尊称后缀'}, _re_compile(r'honorific.*?suffix'),),
        'Home Town': ({'zh': '家乡'}, _re_compile(r'home.*?town'),),
        'Employer': ({'zh': '雇主'}, ['employer'],),
        'Family': ({'zh': '家庭/亲戚'}, ['family', 'house', 'royal house'],),
        'Ethnicity': ({'zh': '种族'}, ['ethnicity', 'ethnic'],),
        'Subject': ({'zh': '学科'}, ['subject', 'discipline'],),
        'Works': ({'zh': '作品'}, ['works'],
                  _re_compile(r'notable.*?works?|associated.*?acts')),
        'Net Worth': ({'zh': '净值'}, _re_compile(r'net.*?worth'),),
        'Awards': ({'zh': '奖项'}, ['prizes'], _re_compile(r'wards?', mode='e'),),
        'Projects': ({'zh': '项目'}, _re_compile(r'projects?', mode='e'),),
        'Institutions': ({'zh': '机构'}, ['agency'], _re_compile(r'institutions?|work.*?institutions?')),
        'School': ({'zh': '学校'}, ['school', 'college'], _re_compile(r'high.*?school')),
        'Hair Color': ({'zh': '发色'}, ['haircolour'], _re_compile(r'hair.*?color')),
        'Eye Color': ({'zh': '眼睛颜色'}, ['eyecolour'], _re_compile(r'eye.*?color')),
        'Measurements': ({'zh': '三围'}, ['measurements'],),
        'Salary': ({'zh': '薪资'}, ['salary']),
        'Party': ({'zh': '政党'}, ['party'],),
        'Car': ({'zh': '汽车'}, ['car']),
        'Ancestry': ({'zh': '祖籍'}, ['ancestry']),
        'Blood Type': ({'zh': '血型'}, _re_compile(r'blood.*?type')),
        'Country': ({'zh': '国家'}, ['country']),
        'Influenced': ({'zh': '受影响'}, ['influenced'],),
        'Influences': ({'zh': '影响'}, ['influences'],),
        'Interests': ({'zh': '兴趣'}, _re_compile(r'main.*?interests?')),
        'Previous Occupation': ({'zh': '以前的职业'}, _re_compile(r'previous.*?occupation')),
        'Title': ({'zh': '头衔'}, ['title']),
        'Status': ({'zh': '状态'}, ['status', 'dead'],),
        'Company': ({'zh': '公司'}, ['company']),
        'Type': ({'zh': '种类'}, ['type']),
    }
    multi_values_field = None

    _dont_parse = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading]

    def __init__(self, values, entry, multi_dict=None):
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
                            groups = [int(i) for i in res.groups() if i]
                            if groups:
                                index = groups.pop()
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
                            groups = [int(i) for i in res.groups() if i]
                            if groups:
                                index = groups.pop()
                            field = kk
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
                                    v['values'][iii] = {str(0) + str(iii): v['values'][iii]}
                                    # v['values'][iii] = {0: v['values'][iii]}
                                    # break
                            multi_values_field[i_k]['values'].append({k: v['values']})
            for v in multi_values_field.values():
                if v['values']:
                    v['values'] = _get_multi_values(v['values'])
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
                                v['values'][iii] = {str(0) + str(iii): v['values'][iii]}
                                # v['values'][iii] = {0: v['values'][iii]}
                                # break
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
                                                     'values': _get_multi_values(multi_values_field)}})
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

                    if _is_int(str(k.name).strip(' ')) and str(k.value).strip(' ') not in ['zh-hans']:
                        values.append(str(k.value).strip(' '))
                    elif str(k.name).strip(' ') in ['m', 'end', 'reason', 'award', 'ft', 'in', 'meter', 'meters', 'cm']:
                        values.append(f"({str(k.name).strip(' ')}: {str(k.value).strip(' ')})")
                if re.search(r'medal', str(j.name).strip().lower()):
                    res = f"({str(j.name).strip()}: {', '.join(values)})"
                else:
                    res = ', '.join(values)
                p_t[i] = mwp.parse(res)
            elif isinstance(j, mwp.wikicode.ExternalLink):
                p_t[i] = j.url
            elif isinstance(j, mwp.wikicode.Tag):
                rs = mwp.parse('\n') if str(j.tag) == 'br' else mwp.parse(str(j.contents).strip(' '))
                p_t[i] = rs
            elif isinstance(j, mwp.wikicode.Wikilink):
                p_t[i] = mwp.parse(str(j.title).strip(' '))
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
        'Label': ({'zh': '唱片公司'}, ['label'],),
        'Instrument': ({'zh': '乐器'}, ['instrument', 'instruments'],),
        'Voice Type': ({'zh': '声音类型'}, _re_compile(r'voice.*?type'),),
        'Chinese Name': ({'zh': '中文名'}, _re_compile(r'chinese.*?name'),),
        'Notable Role': ({'zh': '著名角色'}, _re_compile(r'notable.*?roles?'),),
        'Associated Artists': (
            {'zh': '相关艺术家'}, _re_compile(r'associated.*?act')),
        'Current Members': ({'zh': '现有成员'}, _re_compile(r'current.*?members?'),),
        'Past Members': ({'zh': '过去成员'}, _re_compile(r'past.*?members?'),),
        'English Name': ({'zh': '英文名'}, _re_compile(r'nama.*?inggeris'),),
        'Location': ({'zh': '表演场地/外景拍摄地'}, ['location']),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateRoyalty(TemplateBase):
    template_name = 'Royalty'
    fields_map = {
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding')),
        '_Reign': ({'zh': '在位'}, _re_compile(r'reign'),),
        '_Coronation': ({'zh': '加冕礼'}, _re_compile(r'coronation'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),),
        '_Succession': ({'zh': '继承'}, _re_compile(r'succession'),),
        '_Regent': ({'zh': '摄政'}, _re_compile(r'regent'),),
        'Royal Anthem': ({'zh': '皇家国歌'}, _re_compile(r'royal.*?anthem'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Office': ({'zh': '任职信息'}, ['_Successor', '_Reign', '_Coronation', '_Predecessor', '_Succession', '_Regent']),
        'Native Name': ({'zh': '本地名字'}, ['Native Name'])}


class TemplateModel(TemplateBase):
    template_name = 'Model'
    fields_map = {
        'Dress Size': ({'zh': '服装尺码'}, _re_compile(r'dress.*?size'),),
        'Shoe Size': ({'zh': '鞋子尺码'}, _re_compile(r'shoe.*?size'),),
        'Location': ({'zh': '表演场地/外景拍摄地'}, ['location']),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateMinister(TemplateBase):
    template_name = 'Minister'
    fields_map = {
        '_Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        '_Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Office': ({'zh': '任职信息'}, ['_Office', '_Prime Minister', '_Term Start', '_Predecessor', '_Term End'])}


class TemplateOfficeholder(TemplateBase):
    template_name = 'Officeholder'
    fields_map = {
        '_Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        '_Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        '_Majority': ({'zh': '多数'}, _re_compile(r'majority')),
        '_Assembly': ({'zh': '议会'}, _re_compile(r'assembly')),
        '_State': ({'zh': '州'}, _re_compile(r'state')),
        '_Deputy': ({'zh': '副职'}, _re_compile(r'deputy'),),
        '_Leader': ({'zh': '领导'}, _re_compile(r'leader'),),
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Term': ({'zh': '在位时间'}, _re_compile(r'term'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),),
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding'),),
        '_Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        '_Alongside': ({'zh': '合作'}, _re_compile(r'alongside'),),
        '_President': ({'zh': '总统'}, _re_compile(r'president'),),
        '_Governor': ({'zh': '总督'}, _re_compile(r'governor|governor.*?general'),),
        '_Vice President': ({'zh': '副总统'}, _re_compile(r'vice.*?president'),),
        '_Appointer': ({'zh': '任命者'}, _re_compile(r'appointer'),),
        '_Minister': ({'zh': '部长'}, _re_compile(r'minister'),),
        'Cabinet': ({'zh': '内阁'}, ['cabinet'],),
        'Department': ({'zh': '部门'}, ['department'],),
        'Allegiance': ({'zh': '忠诚'}, _re_compile(r'allegiance')),
        '_Nominator': ({'zh': '提名人'}, _re_compile(r'nominator'),),
        '_Chancellor': ({'zh': '校长'}, _re_compile(r'chancellor'),),
        '_Lieutenant': ({'zh': '中尉'}, _re_compile(r'lieutenant'),),
        '_Appointed': ({'zh': '任职日期'}, _re_compile(r'appointed'),),
        'Service Years': ({'zh': '服务年限'}, _re_compile(r'service.*?years?'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['_Office', '_Deputy', '_Term Start', '_Term End', '_Predecessor', '_Successor',
                                      '_Prime Minister', '_President', '_Governor', '_Alongside', '_Minister',
                                      '_Appointer',
                                      '_Term', '_Chancellor', '_Leader', '_Lieutenant', '_Vice President', '_Nominator',
                                      '_Appointed', '_Monarch', '_Majority', '_Assembly', '_State'])}


class TemplateFootballPlayer(TemplateBase):
    template_name = 'Football Player'
    fields_map = {
        'Player Name': ({'zh': '运动员名称'}, _re_compile(r'player.*?name'),),
        'Current Club': ({'zh': '目前俱乐部'}, _re_compile(r'current.*?club'),),
        'Club Number': ({'zh': '运动员编号'}, _re_compile(r'club.*?number'),),
        'Position': ({'zh': '运动员定位'}, ['position'],),
        '_Years': ({'zh': '服役年份'}, _re_compile(r'years?|club.*?years?'),),
        '_Clubs': ({'zh': '服役俱乐部'}, _re_compile(r'clubs?'),),
        '_Caps(Goals)': ({'zh': '出场数(进球数)'}, _re_compile(r'caps\(goals\)'),),
        '_Caps': ({'zh': '出场数'}, _re_compile(r'caps?'),),
        '_Goals': ({'zh': '进球数'}, _re_compile(r'goals?'),),
        '_National Years': ({'zh': '国家队服役年份'}, _re_compile(r'national.*?years?'),),
        '_National Team': ({'zh': '国家队'}, _re_compile(r'national.*?teams?'),),
        '_National Caps(Goals)': ({'zh': '在国家队出场数(在国家队进球数)'}, _re_compile(r'national.*?caps\(goals\)'),),
        '_Youth Clubs': ({'zh': '青年俱乐部'}, _re_compile(r'youth.*?clubs?'),),
        '_Youth Years': ({'zh': '青年俱乐部服役年份'}, _re_compile(r'youth.*?years?'),),
        '_Youth Caps(Goals)': ({'zh': '在青年俱乐部出场数(在青年俱乐部进球数)'}, _re_compile(r'youth.*?caps\(goals\)'),),
        '_Youth Caps': ({'zh': '在青年俱乐部出场数'}, _re_compile(r'youth.*?caps?'),),
        '_Youth Goals': ({'zh': '在青年俱乐部进球数'}, _re_compile(r'youth[-_\s]*goals?'),),
        '_National Caps': ({'zh': '在国家队出场数'}, _re_compile(r'national.*?caps?'),),
        '_National Goals': ({'zh': '在国家队进球数'}, _re_compile(r'national[-_\s]*goals?'),),
        'Total Caps': ({'zh': '总出场数'}, _re_compile(r'total.*?caps?'),),
        'Total Goals': ({'zh': '总进球数'}, _re_compile(r'total.*?goals?'),),
        '_Manager Clubs': ({'zh': '管理俱乐部'}, _re_compile(r'manager.*?clubs?'),),
        '_Manager Years': ({'zh': '管理俱乐部年份'}, _re_compile(r'manager.*?years?'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Clubs': ({'zh': '服役俱乐部'}, ['_Years', '_Clubs', '_Caps', '_Goals', '_Caps(Goals)']),
                          'National Team': (
                              {'zh': '服役国家队'},
                              ['_National Years', '_National Team', '_National Caps', '_National Goals',
                               '_National Caps(Goals)']),
                          'Youth Clubs': ({'zh': '服役青年俱乐部'},
                                          ['_Youth Clubs', '_Youth Years', '_Youth Caps(Goals)', '_Youth Caps',
                                           '_Youth Goals']),
                          'Manager Clubs': ({'zh': '管理俱乐部'}, ['_Manager Clubs', '_Manager Years'])}


class TemplateFootballOfficial(TemplateBase):
    template_name = 'Football Official'
    fields_map = {
        '_League': ({'zh': '联盟'}, _re_compile(r'league'),),
        '_Role': ({'zh': '角色'}, _re_compile(r'roles?'),),
        '_Years': ({'zh': '年份'}, _re_compile(r'years?'),),
        '_International Years': ({'zh': '国际年份'}, _re_compile(r'international.*?years'),),
        '_International League': ({'zh': '国际联盟'}, _re_compile(r'confederation'),),
        '_International Role': ({'zh': '国际角色'}, _re_compile(r'international.*?roles?'),)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'League': ({'zh': '联盟'}, ['_League', '_Role', '_Years']),
        'International League': (
            {'zh': '国际联盟'}, ['_International League', '_International Role', '_International Years'])
    }


class TemplateAdultBiography(TemplateBase):
    template_name = 'Adult Biography'
    fields_map = {
        'Number Films': ({'zh': '电影数目'}, _re_compile(r'number.*?films'),),
        'Orientation': ({'zh': '性取向'}, ['orientation'],),
        'Films': ({'zh': '电影'}, ['films', 'film'],),
        'Location': ({'zh': '表演场地/外景拍摄地'}, ['location']),
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
        'Location': ({'zh': '表演场地/外景拍摄地'}, ['location']),
        'Label': ({'zh': '唱片公司'}, ['label'],),
        'Genre': ({'zh': '类型'}, ['genre'],),
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
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateVicePresident(TemplateBase):
    template_name = 'Vice President'
    fields_map = {
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding'),),
        '_President': ({'zh': '总统'}, _re_compile(r'president'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['_Term Start', '_Term End', '_Successor', '_President', '_Predecessor'])}


class TemplateSwimmer(TemplateBase):
    template_name = 'Swimmer'
    fields_map = {
        'Medal': ({'zh': '奖牌'}, _re_compile(r'medal.*?templates?'),),
        '_National Team': ({'zh': '国家队'}, _re_compile(r'national.*?teams?'),),
        '_National Years': ({'zh': '国家队服役年份'}, _re_compile(r'national.*?years?'),),
        'Coach': ({'zh': '教练'}, ['coach'],)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'National Team': (
        {'zh': '服役国家队'}, ['_National Years', '_National Team'])}


class TemplateIndonesiaArtist(TemplateBase):
    template_name = 'Indonesia Artist'
    fields_map = {
        'Instrument': ({'zh': '乐器'}, ['instrument', 'instruments'],),
        'Label': ({'zh': '唱片公司'}, ['label'],),
        'Genre': ({'zh': '类型'}, ['genre'],),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplatePrimeMinister(TemplateBase):
    template_name = 'Prime Minister'
    fields_map = {
        '_Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        '_Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        '_Deputy': ({'zh': '副职'}, _re_compile(r'deputy'),),
        '_Leader': ({'zh': '领导'}, _re_compile(r'leader'),),
        '_Assembly': ({'zh': '议会'}, _re_compile(r'assembly')),
        '_Majority': ({'zh': '多数'}, _re_compile(r'majority')),
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),),
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding'),),
        '_Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        '_President': ({'zh': '总统'}, _re_compile(r'president'),),
        '_Governor': ({'zh': '总督'}, _re_compile(r'governor|governor.*?general'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['_Deputy', '_Term Start', '_Term End', '_Predecessor', '_Successor', '_President',
                                      '_Prime Minister', '_Office', '_Leader', '_Monarch', '_Majority', '_Assembly',
                                      '_Governor'])}


class TemplateMP(TemplateBase):
    template_name = 'Member of Parliament'
    fields_map = {
        '_Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        '_Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        '_Majority': ({'zh': '多数'}, _re_compile(r'majority')),
        '_Deputy': ({'zh': '副职'}, _re_compile(r'deputy'),),
        '_Assembly': ({'zh': '议会'}, _re_compile(r'assembly')),
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),),
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding'),),
        '_Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        '_Minister': ({'zh': '部长'}, _re_compile(r'minister'),),
        '_President': ({'zh': '总统'}, _re_compile(r'president'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['_Office', '_Term Start', '_Term End', '_Predecessor', '_Successor', '_Minister',
                                      '_Deputy', '_Prime Minister', '_President', '_Monarch', '_Majority',
                                      '_Assembly'])}


class TemplateScientist(TemplateBase):
    template_name = 'Scientist'
    fields_map = {
        'Workplace': ({'zh': '工作地'}, _re_compile(r'work.*?places?')),
        '_Thesis Year': ({'zh': '论文年份'}, _re_compile(r'thesis.*?years?')),
        '_Thesis Title': ({'zh': '论文标题'}, _re_compile(r'thesis.*?titles?')),
        '_Thesis Url': ({'zh': '论文链接'}, _re_compile(r'thesis.*?urls?')),
        'Fields': ({'zh': '领域'}, ['field', 'fields']),
        'Academic Advisors': ({'zh': '学术顾问'}, _re_compile(r'academic.*?advisors?')),
        'Doctoral Advisors': ({'zh': '博士生导师'}, _re_compile(r'doctoral.*?advisors?')),
        'Boards': ({'zh': '董事会'}, ['boards']),
        'Doctoral Students': ({'zh': '博士生'}, _re_compile(r'doctoral.*?students?')),
        'Notable Students': ({'zh': '著名学生'}, _re_compile(r'notable.*?students?'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Thesis': ({'zh': '论文'}, ['_Thesis Title', '_Thesis Year', '_Thesis Url'])
    }


class TemplateEconomist(TemplateBase):
    template_name = 'Economist'
    fields_map = {
        'Fields': ({'zh': '领域'}, ['field', 'fields']),
        'Contributions': ({'zh': '贡献'}, ['contributions', 'contribution']),
        'Doctoral Students': ({'zh': '博士生'}, _re_compile(r'doctoral.*?students?')),
        'Doctoral Advisors': ({'zh': '博士生导师'}, _re_compile(r'doctoral.*?advisors?')),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateGovernor(TemplateBase):
    template_name = 'Governor'
    fields_map = {
        '_Deputy': ({'zh': '副职'}, _re_compile(r'deputy'),),
        '_Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        '_Lieutenant': ({'zh': '中尉'}, _re_compile(r'lieutenant'),),
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding')),
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Vice Governor': ({'zh': '副总督'}, _re_compile(r'vice.*?governor')),
        '_Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),),
        '_President': ({'zh': '总统'}, _re_compile(r'president'),),
        '_Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Office': ({'zh': '职位信息'}, ['_Deputy', '_Monarch', '_Lieutenant', '_Successor',
                                    '_Term Start', '_Vice Governor', '_Office', '_Predecessor',
                                    '_President', '_Prime Minister', '_Term End'])
    }


class TemplateSenator(TemplateBase):
    template_name = 'Senator'
    fields_map = {
        '_State': ({'zh': '州'}, _re_compile(r'state')),
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'}, ['_State', '_Term Start', '_Term End', '_Successor'])}


class TemplateGolfer(TemplateBase):
    template_name = 'Golfer'
    fields_map = {
        '_Years': ({'zh': '获奖年份'}, _re_compile(r'years?'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Awards': ({'zh': '奖项'}, ['Awards', '_Years'])
    }


class TemplateFieldHockeyPlayer(TemplateBase):
    template_name = 'Field Hockey Player'
    fields_map = {
        'Position': ({'zh': '运动员定位'}, ['position'],),
        '_Years': ({'zh': '服役年份'}, _re_compile(r'years?|club.*?years?'),),
        '_Clubs': ({'zh': '服役俱乐部'}, _re_compile(r'clubs?'),),
        '_Caps': ({'zh': '出场数'}, _re_compile(r'caps?'),),
        '_Goals': ({'zh': '进球数'}, _re_compile(r'goals?'),),
        '_National Years': ({'zh': '国家队服役年份'}, _re_compile(r'national.*?years?'),),
        '_National Team': ({'zh': '国家队'}, _re_compile(r'national.*?teams?'),),
        '_National Caps': ({'zh': '在国家队出场数'}, _re_compile(r'national.*?caps?'),),
        '_National Goals': ({'zh': '在国家队进球数'}, _re_compile(r'national[-_\s]*goals?'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Clubs': ({'zh': '服役俱乐部'}, ['_Years', '_Clubs', '_Caps', '_Goals']),
                          'National Team': (
                              {'zh': '服役国家队'},
                              ['_National Years', '_National Team', '_National Caps', '_National Goals'])}


class TemplateTennisPlayer(TemplateBase):
    template_name = 'Tennis Player'
    fields_map = {
        'Player Name': ({'zh': '运动员名称'}, _re_compile(r'player.*?name'),),
        'Competition': ({'zh': '比赛信息'}, _re_compile(r'results?', mode='e')),
        'Coach': ({'zh': '教练'}, ['coach']),
        'Style': ({'zh': '风格'}, _re_compile(r'plays?')),
        'Turned Pro': ({'zh': '成为职业选手'}, _re_compile(r'turned.*?pro')),
        'Career Prize Money': ({'zh': '职业奖金'}, _re_compile(r'career.*?prize.*?money')),
        'Singles Record': ({'zh': '单打纪录'}, _re_compile(r'single.*?record')),
        'Singles Titles': ({'zh': '单打冠军'}, _re_compile(r'single.*?titles?')),
        'Highest Singles Ranking': ({'zh': '最高单打排名'}, _re_compile(r'highest.*?single.*?ranking')),
        'Current Singles Ranking': ({'zh': '目前单打排名'}, _re_compile(r'current.*?single.*?ranking')),
        'Doubles Record': ({'zh': '双打记录'}, _re_compile(r'double.*?record')),
        'Doubles Titles': ({'zh': '双打冠军'}, _re_compile(r'double.*?titles?')),
        'Highest Doubles Ranking': ({'zh': '最高双打排名'}, _re_compile(r'highest.*?double.*?ranking')),
        'Current Doubles Ranking': ({'zh': '目前双打排名'}, _re_compile(r'current.*?double.*?ranking')),
        'Mixed Titles': ({'zh': '混打冠军'}, _re_compile(r'mixed.*?titles?')),
        'Mixed Record': ({'zh': '混打记录'}, _re_compile(r'mixed.*?record'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateBoxer(TemplateBase):
    template_name = 'Boxer'
    fields_map = {
        'Ko': ({'zh': 'ko胜利次数'}, ['ko']),
        'Total': ({'zh': '总次数'}, ['total']),
        'Style': ({'zh': '风格'}, ['style']),
        'Wins': ({'zh': '获胜次数'}, _re_compile(r'wins?')),
        'Draws': ({'zh': '平局次数'}, _re_compile(r'draws?')),
        'Losses': ({'zh': '失败次数'}, _re_compile(r'losses|loss'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateTwitchStreamer(TemplateBase):
    template_name = 'Twitch Streamer'
    fields_map = {
        'Channel Name': ({'zh': '频道名'}, _re_compile(r'channel.*?name')),
        'Followers': ({'zh': '订阅者'}, _re_compile(r'followers?')),
        'Views': ({'zh': '观看数'}, _re_compile(r'views?'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplatePhilosopher(TemplateBase):
    template_name = 'Philosopher'
    fields_map = {
        'Notable Ideas': ({'zh': '著名想法'}, _re_compile(r'notable.*?ideas?')),
        'Philosophy': ({'zh': '哲学'}, ['region'])
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateAstronaut(TemplateBase):
    template_name = 'Astronaut'
    fields_map = {
        'Mission': ({'zh': '使命'}, ['mission']),
        'Space Time': ({'zh': '时间'}, ['time'], _re_compile(r'space.*?time')),
        'Selection': ({'zh': '选拔'}, ['selection']),
        'Rank': ({'zh': '等级'}, ['rank']),
        '_Eva': ({'zh': '舱外活动'}, _re_compile(r'evas?|eva.*?time')),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Eva': ({'zh': '舱外活动'}, ['_Eva'])
    }


class TemplateJudge(TemplateBase):
    template_name = 'Judge'
    fields_map = {
        '_Appointer': ({'zh': '任命者'}, _re_compile(r'appointer'),),
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Nominator': ({'zh': '提名人'}, _re_compile(r'nominator'),),
        '_Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['_Office', '_Term Start', '_Term End', '_Predecessor', '_Successor', '_Nominator',
                                      '_Appointer'])}


class TemplatePresident(TemplateBase):
    template_name = 'President'
    fields_map = {
        '_Prime Minister': ({'zh': '总理'}, _re_compile(r'prime.*?minister'),),
        '_Vice President': ({'zh': '副总统'}, _re_compile(r'vice.*?president'),),
        '_Term Start': ({'zh': '开始时间'}, _re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '结束时间'}, _re_compile(r'term.*?end'),),
        '_Office': ({'zh': '职位'}, _re_compile(r'office|order'),),
        '_Successor': ({'zh': '后任'}, ['heir'], _re_compile(r'successor|succeeded|succeeding'),),
        '_Lieutenant': ({'zh': '中尉'}, _re_compile(r'lieutenant'),),
        '_Predecessor': ({'zh': '前任'}, _re_compile(r'predecessor|preceded|preceding'),),
        '_Assembly': ({'zh': '议会'}, _re_compile(r'assembly')),
        '_Term': ({'zh': '在位时间'}, _re_compile(r'term'),),
        '_Alongside': ({'zh': '合作'}, _re_compile(r'alongside'),),
        '_President': ({'zh': '总统'}, _re_compile(r'president'),),
        '_Monarch': ({'zh': '君主'}, _re_compile(r'monarch')),
        '_State': ({'zh': '州'}, _re_compile(r'state')),
        '_Leader': ({'zh': '领导'}, _re_compile(r'leader'),),
        'Service Years': ({'zh': '服务年限'}, _re_compile(r'service.*?years?')),
        'Rank': ({'zh': '等级'}, ['rank']),
        'Allegiance': ({'zh': '忠诚'}, _re_compile(r'allegiance')),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '任职信息'},
                                     ['_Office', '_Term Start', '_Term End', '_Predecessor', '_Successor',
                                      '_Prime Minister', '_President', '_Alongside',
                                      '_Term', '_Leader', '_Lieutenant', '_Vice President',
                                      '_Monarch', '_Assembly', '_State'])}


class TemplateCelebrity(TemplateBase):
    template_name = 'Celebrity'


class TemplateSquashPlayer(TemplateBase):
    template_name = 'Squash Player'
    fields_map = {
        'Date Of Current Ranking': (
            {'zh': '目前排名日期'}, _re_compile(r'date.*?current.*?ranking|current.*?ranking.*?date')),
        'Date Of Highest Ranking': (
            {'zh': '最高排名日期'}, _re_compile(r'highest.*?ranking.*?date|date.*?highest.*?ranking')),
        'Turned Pro': ({'zh': '成为职业选手'}, _re_compile(r'turned.*?pro')),
        'Medal': ({'zh': '奖牌'}, _re_compile(r'medal.*?templates?'),),
        'Racquet': ({'zh': '球拍'}, ['racquet']),
        'Finals': ({'zh': '决赛'}, ['finals', 'final']),
        'Titles': ({'zh': '冠军'}, ['titles']),
        'Highest Ranking': ({'zh': '最高排名'}, _re_compile(r'highest.*?ranking')),
        'Coach': ({'zh': '教练'}, ['coach'],),
        'Current Ranking': ({'zh': '目前排名'}, _re_compile(r'current.*?ranking')),
        'Style': ({'zh': '风格'}, _re_compile(r'plays?')),
        'Competition': ({'zh': '比赛信息'}, _re_compile(r'results?', mode='e')),
        'Event': ({'zh': '比赛项目'}, ['event'])
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateF1Driver(TemplateBase):
    template_name = 'F1 Driver'
    fields_map = {
        '_Car Number': ({'zh': '车号'}, _re_compile(r'car.*?number')),
        'Years': ({'zh': '年份'}, _re_compile(r'years?')),
        'Last Win': ({'zh': '最后一次胜利'}, _re_compile(r'last.*?win')),
        'Championships': ({'zh': '锦标赛'}, _re_compile(r'championships?')),
        'Poles': ({'zh': '极点'}, _re_compile(r'poles?')),
        '_Teams': ({'zh': '团队'}, ['team(s)'], _re_compile(r'teams?')),
        'First Win': ({'zh': '第一次胜利'}, _re_compile(r'first.*?win')),
        'Last Season': ({'zh': '最后一个赛季'}, _re_compile(r'last.*?season')),
        'Races': ({'zh': '竞赛信息'}, _re_compile(r'races?')),
        'Fastest Laps': ({'zh': '最快圈速'}, _re_compile(r'fastest.*?laps?')),
        'Last Race': ({'zh': '最后一场竞赛'}, _re_compile(r'last.*?race')),
        'First Race': ({'zh': '第一场竞赛'}, _re_compile(r'first.*?race')),
        'Wins': ({'zh': '获胜次数'}, _re_compile(r'wins?')),
        'Podiums': ({'zh': '领奖台次数'}, _re_compile(r'podiums?')),
        'Points': ({'zh': '点/分'}, _re_compile(r'points?')),
        'Last Position': ({'zh': '最后位置'}, _re_compile(r'last.*?position'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Teams': ({'zh': '团队'}, ['_Teams', '_Car Number'])
    }


class TemplateJournalist(TemplateBase):
    template_name = 'Journalist'


class TemplateFashionDesigner(TemplateBase):
    template_name = 'Fashion Designer'
    fields_map = {
        'Tag': ({'zh': '标签'}, _re_compile(r'label.*?name'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateMilitaryPerson(TemplateBase):
    template_name = 'Military Person'
    fields_map = {
        'Office': ({'zh': '任职信息'}, _re_compile(r'commands?')),
        'Branch': ({'zh': '政府分支'}, _re_compile(r'branch')),
        'Unit': ({'zh': '小队'}, _re_compile(r'unit')),
        'Allegiance': ({'zh': '忠诚'}, _re_compile(r'allegiance')),
        'Service Years': ({'zh': '服务年限'}, _re_compile(r'service.*?years?')),
        'Battles': ({'zh': '战争'}, _re_compile(r'battles?')),
        'Rank': ({'zh': '等级'}, ['rank']),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateVideoGamePlayer(TemplateBase):
    template_name = 'Video Game Player'
    fields_map = {
        'Role': ({'zh': '角色'}, _re_compile(r'roles?'),),
        '_Years': ({'zh': '年份'}, _re_compile(r'years?')),
        '_Teams': ({'zh': '团队'}, _re_compile(r'teams?')),
        '_Coach Years': ({'zh': '教练年份'}, _re_compile(r'cyears?')),
        '_Coach Teams': ({'zh': '教练团队'}, _re_compile(r'cteams?')),
        'League': ({'zh': '联盟'}, _re_compile(r'leagues?')),
        'Games': ({'zh': '游戏'}, _re_compile(r'games?'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Teams': ({'zh': '团队'}, ['_Teams', '_Years']),
        'Coach Teams': ({'zh': '教练团队'}, ['_Coach Teams', '_Coach Years'])
    }


class TemplateSportPerson(TemplateBase):
    template_name = 'Sport Person'
    fields_map = {
        'Head Coach': ({'zh': '总教练'}, _re_compile(r'head.*?coach')),
        'Clubs': ({'zh': '服役俱乐部'}, _re_compile(r'clubs?')),
        'Sports': ({'zh': '运动'}, _re_compile(r'sports?')),
        'Medal': ({'zh': '奖牌'}, _re_compile(r'medal.*?templates?'),),
        'Teams': ({'zh': '团队'}, _re_compile(r'teams?')),
        'Coach': ({'zh': '教练'}, ['coach'], _re_compile(r'former.*?coach')),
        'Training': ({'zh': '训练'}, ['training']),
        'College Team': ({'zh': '大学团队'}, _re_compile(r'college.*?teams?')),
        'Event': ({'zh': '比赛项目'}, ['event']),
        'Position': ({'zh': '运动员定位'}, ['position'],)
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
                             'infobox football biography 2', 'infobox biografi bolasepak'],
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
    TemplateFieldHockeyPlayer: ['infobox field hockey player'],
    TemplateTennisPlayer: ['infobox tennis biography', 'infobox tennis player'],
    TemplateBoxer: ['infobox peninju', 'infobox boxer'],
    TemplateTwitchStreamer: ['infobox twitch streamer'],
    TemplatePhilosopher: ['infobox philosopher', 'infobox philosopher'],
    TemplateAstronaut: ['infobox angkasawan', 'infobox astronaut'],
    TemplateJudge: ['infobox judge'],
    TemplatePresident: ['infobox president', 'infobox_president'],
    TemplateCelebrity: ['infobox celebrity', 'infobox_celebrity'],
    TemplateSquashPlayer: ['infobox squash player'],
    TemplateF1Driver: ['infobox f1 driver'],
    TemplateJournalist: ['infobox journalist'],
    TemplateFashionDesigner: ['infobox fashion designer'],
    TemplateMilitaryPerson: ['infobox military person'],
    TemplateVideoGamePlayer: ['infobox video game player'],
    TemplateSportPerson: ['infobox sportsperson']
}

TEMPLATE_MAP = {i: k for k, v in _TEMPLATE_MAP.items() for i in v}

MULTI_DICT = {i.template_name: [] for i in _TEMPLATE_MAP.keys()}

if __name__ == '__main__':
    value = {
        "name": "David Boudia",
        "image": "David Boudia at the 2016 Summer Olympics – Men's synchronized 10 metre platform.jpg",
        "fullname": "David Alasdair Boudia",
        "country": "{{USA}}",
        "birth_date": "{{Birth date and age|1989|4|24}}",
        "birth_place": "[[Abilene, Texas]]",
        "hometown": "[[Noblesville, Indiana]]",
        "training": "[[West Lafayette, Indiana]]",
        "height": "{{height|ft=5|in=9}}",
        "event": "10m, 10m segerak",
        "club": "National Training Center",
        "collegeteam": "[[Purdue University]]",
        "partner": "[[Steele Johnson]]",
        "former_partner": "[[Nick McCrory]],[[Thomas Finchum]]",
        "headcoach": "Adam Soldati,\nJohn Wingfield",
        "medaltemplates": "{{MedalCompetition|[[Sukan Olimpik]]}}\n{{MedalGold|[[Sukan Olimpik Musim Panas 2012|2012 London]]|[[Terjun di Sukan Olimpik Musim Panas 2012|10 m platform]]}}\n{{MedalBronze|[[Sukan Olimpik Musim Panas 2012|2012 London]]|[[Terjun di Sukan Olimpik Musim Panas 2012|10 m segerak]]}}\n{{MedalCompetition|Kejohanan Dunia Akuatik}}\n{{MedalSilver|[[Diving at the 2009 World Aquatics Championships|2009 Rome]]|10 m segerak}}\n{{MedalSilver|[[Diving at the 2011 World Aquatics Championships|2011 Shanghai]]|10 m}}\n{{MedalSilver|[[Diving at the 2013 World Aquatics Championships|2013 Barcelona]]|10 m}}\n{{MedalSilver|[[Diving at the 2015 World Aquatics Championships|2015 Kazan]]|10 m}}\n{{MedalBronze|[[Diving at the 2007 World Aquatics Championships|2007 Melbourne]]|10 m segerak}}\n{{MedalCompetition|Pan American Games}}\n{{MedalGold|[[Diving at the 2007 Pan American Games|2007 Rio]]|10 m segerak}}\n{{MedalCompetition|[[Piala Dunia Terjun FINA]]}}\n{{MedalGold|[[2010 FINA Diving World Cup|2010 Changzhou]]|Pasukan}}\n{{MedalBronze|[[2008 FINA Diving World Cup|2008 Beijing]]|10 m platform}}"
    }
    tem = TemplateSportPerson(value, 'Test')
    # print(tem.fields)
    for i in tem.fields['fields']['Medal']['values']:
        print(i, '\n')
    # print(tem.graph_entities)
