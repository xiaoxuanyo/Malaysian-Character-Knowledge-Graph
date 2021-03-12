# -*- coding: utf-8 -*-
"""
@time   : 2021-3-11 14:14
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import mwparserfromhell as mwp
import pywikibot
from src.utils import LoggerUtil
import logging
import re

__all__ = ['re_compile', 'LoggerUtil', 'mwp', 'QueryEngine', 'TemplateBase',
           'TemplateOfficer', 'TemplateSportsPlayer', 'TemplatePerformanceWorker',
           'TemplateResearchers']

_FILE_LOG_LEVEL = logging.WARNING
_CONSOLE_LOG_LEVEL = logging.WARNING

_file_log = LoggerUtil('src.templates.file', file_path='../log/templates.log',
                       level=_FILE_LOG_LEVEL, mode='a+')
_console_log = LoggerUtil('src.templates.console', level=_CONSOLE_LOG_LEVEL)


def _is_int(string):
    try:
        int(string)
        return True
    except (TypeError, ValueError):
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


def re_compile(s, mode='se', split='.*?'):
    assert mode in ['s', 'e', 'se'], f'不支持{mode}'
    _s = r'^'
    _e = r'$'
    if mode == 's':
        _p = _s + '%s'
    elif mode == 'e':
        _p = '%s' + _e
    else:
        _p = _s + '%s' + _e
    s = s.split('|')
    ss = []
    for j, i in enumerate(s):
        i_split = i.split(split)
        index = []
        for k in range(len(i_split) - 1):
            index.append('i' + str(j))
            index.append(str(j + k))
        ss.append(r'\s*?(?P<s_index%d>\d*)\s*?' % j + r'\D*?(?P<%s_index%s>\d*)\D*?'.join(
            i_split) % tuple(index) + r'\s*?(?P<e_index%d>\d*)\s*?' % j)
    s = '|'.join([_p % j for j in ss])
    return re.compile(r'%s' % s)


def _matches(string, match):
    def match1(i_s, i_m):
        assert isinstance(i_m, list) or isinstance(i_m, re.Pattern), f'类型不符，match类型{type(i_m)}'
        if isinstance(i_m, list):
            if i_s in i_m:
                return True, None
            else:
                return False, None
        else:
            res = re.search(i_m, i_s)
            if res:
                return True, res
            else:
                return False, None

    def match2(i_s, m_l, m_r):
        assert isinstance(m_l, list) and isinstance(m_r,
                                                    re.Pattern), f'类型不符，match[0]类型{type(m_l)}，match[1]类型{type(m_r)}'
        if i_s in m_l:
            return True, None
        elif re.search(m_r, i_s):
            return True, re.search(m_r, i_s)
        else:
            return False, None

    assert isinstance(match, tuple), f'不支持的match类型{type(match)}'
    if len(match) == 1:
        return match1(string, match[0])
    elif len(match) == 2:
        if isinstance(match[0], dict):
            return match1(string, match[1])
        else:
            return match2(string, match[0], match[1])
    elif len(match) == 3:
        return match2(string, match[1], match[2])
    else:
        raise ValueError(f'不支持的match参数, {match}')


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
    # 模板名称，在构建图谱时模板名会当成节点的标签名
    template_name = 'Base'
    # 定义需要获取的字段，以下划线开头的字段表示为多值属性字段
    # 元组中第一个字典形式的数据在构建图谱时是作为边的公共属性
    fields_map = {
        'Name': ({'zh': '名字'}, ['name', 'nama'],),
        'Alias': (
            {'zh': '别名'}, ['alias', 'nickname', 'hangul', 'id', 'pseudonym'],
            re_compile(r'other.*?names?|real.*?name')),
        'Native Name': ({'zh': '本地名字'}, re_compile(r'native.*?names?'),),
        'Birth': ({'zh': '出生信息'}, ['birth', 'born'],),
        'Death': ({'zh': '死亡信息'}, ['died']),
        'Birth Name': ({'zh': '出生名'}, re_compile(r'birth.*?names?'),),
        'Birth Date': ({'zh': '出生日期'}, re_compile(r'birth.*?date|date.*?birth'),),
        'Birth Place': ({'zh': '出生地点'}, ['tempat lahir'], re_compile(r'birth.*?place|place.*?birth')),
        'Retirement Date': ({'zh': '退休时间'}, ['retired'], re_compile(r'date.*?ret')),
        'Birth City': ({'zh': '出生城市'}, re_compile(r'birth.*?city|city.*?birth'),),
        'Birth Country': ({'zh': '出生国家'}, re_compile(r'birth.*?country|country.*?birth'),),
        'Height': ({'zh': '身高'}, ['height'],),
        'Weight': ({'zh': '体重'}, ['weight'],),
        'Nationality': ({'zh': '国籍/民族'}, ['nationality'],),
        'Website': ({'zh': '网站'}, ['website', 'url', 'homepage'],),
        'Origin': ({'zh': '出身/身世/血统'}, ['origin'],),
        'Religion': ({'zh': '宗教'}, ['religion', 'agama'],),
        'Education': ({'zh': '教育'}, ['education', 'pendidikan'],),
        'Occupation': ({'zh': '职业/工作'}, ['occupation', 'occupation(s)', 'pekerjaan', 'ocupation', 'occuption',
                                         'occuoation', 'profession'], re_compile(r'current.*?occupation')),
        'Years Active': ({'zh': '活跃年份'}, ['active', 'yeaesactive', 'era'], re_compile(r'year.*?active')),
        'Death Date': ({'zh': '死亡日期'}, re_compile(r'death.*?date|date.*?death'),),
        'Death Place': ({'zh': '死亡时间'}, re_compile(r'death.*?place|place.*?death'),),
        'Burial Place': ({'zh': '埋葬地点'}, re_compile(r'resting.*?place|burial.*?place'),),
        'Spouse': ({'zh': '配偶'}, ['spouse', 'pasangan', 'spouses', 'consort'],),
        'Parents': ({'zh': '父母'}, ['parents'],),
        'Sibling': ({'zh': '兄弟姐妹'}, ['sibling']),
        'Children': ({'zh': '孩子'}, ['children', 'issue'],),
        'Gender': ({'zh': '性别'}, ['gender'],),
        'Alma Mater': ({'zh': '母校'}, re_compile(r'alma.*?mater'),),
        'Relatives': ({'zh': '关系'}, ['relatives,husband'], re_compile(r'relatives?|relations?'),),
        'Full Name': ({'zh': '全名'}, re_compile(r'full.*?name'),),
        'Father': ({'zh': '父亲'}, ['father', 'bapa'],),
        'Mother': ({'zh': '目前'}, ['mother'],),
        'Residence': ({'zh': '住宅/(尤指)豪宅'}, ['residence', 'residential'],),
        'Known For': ({'zh': '著名'}, ['known'], re_compile(r'known.*?for'),),
        'Partner': ({'zh': '伙伴/搭档/合伙人'}, ['partner'], re_compile(r'former.*?partner|domestic.*?partner')),
        'Citizenship': ({'zh': '公民/公民身份'}, ['citizenship'],),
        'Honorific Prefix': ({'zh': '尊称前缀'}, re_compile(r'honorific.*?prefix'),),
        'Honorific Suffix': ({'zh': '尊称后缀'}, re_compile(r'honorific.*?suffix'),),
        'Home Town': ({'zh': '家乡'}, re_compile(r'home.*?town'),),
        'Employer': ({'zh': '雇主'}, ['employer'],),
        'Family': ({'zh': '家庭/亲属'}, ['family', 'house', 'royal house'],),
        'Ethnicity': ({'zh': '种族'}, ['ethnicity', 'ethnic'],),
        'Subject': ({'zh': '学科'}, ['subject', 'discipline'],),
        'Works': ({'zh': '作品'}, ['works'],
                  re_compile(r'notable.*?works?')),
        'Net Worth': ({'zh': '净值'}, re_compile(r'net.*?worth'),),
        'Awards': ({'zh': '奖项'}, ['prizes'], re_compile(r'wards?', mode='e'),),
        'Projects': ({'zh': '项目'}, re_compile(r'projects?', mode='e'),),
        'Institutions': (
            {'zh': '机构（包括大学、银行等规模大的机构以及代理机构和工作机构）'}, ['agency'], re_compile(r'institutions?|work.*?institutions?')),
        'School': ({'zh': '学校'}, ['school', 'college'], re_compile(r'high.*?school')),
        'Hair Color': ({'zh': '发色'}, ['haircolour'], re_compile(r'hair.*?color')),
        'Eye Color': ({'zh': '眼睛颜色'}, ['eyecolour'], re_compile(r'eye.*?color')),
        'Measurements': ({'zh': '三围'}, ['measurements'],),
        'Salary': ({'zh': '薪资'}, ['salary']),
        'Party': ({'zh': '政党'}, ['party'],),
        'Car': ({'zh': '汽车'}, ['car']),
        'Ancestry': ({'zh': '祖籍'}, ['ancestry']),
        'Blood Type': ({'zh': '血型'}, re_compile(r'blood.*?type')),
        'Country': ({'zh': '国家'}, ['country']),
        'Influenced': ({'zh': '受影响'}, ['influenced'],),
        'Influences': ({'zh': '影响'}, ['influences'],),
        'Interests': ({'zh': '兴趣'}, re_compile(r'main.*?interests?')),
        'Previous Occupation': ({'zh': '以前的职业'}, re_compile(r'previous.*?occupation|previous.*?post')),
        'Title': ({'zh': '头衔/职称'}, ['title']),
        'Status': ({'zh': '状态'}, ['status', 'dead'],),
        'Company': ({'zh': '公司'}, ['company']),
        'Type': ({'zh': '种类/类型'}, ['type']),
    }
    # 多值属性字段
    multi_values_field = None
    # 在解析时跳过的类型
    dont_parse_type = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading]
    # 解析wiki对象template时需要保存的模板名，通常情况下是因为模板名保存了必要的信息，比如某次比赛中的名次（金牌、银牌等）保存在模板名中
    retain_template_name = (re.compile(r'medal'),)
    # 解析wiki对象template时需要剔除的特殊值，这些值往往无意义
    discard_template_value = (['zh-hans'],)
    # 解析wiki对象WikiLink时需要剔除的值，这些值往往无意义
    discard_wikilink_value = (re.compile(r'\.svg$'),)
    # 解析wiki对象template时需要保存的参数名，通常情况下是因为身高体重等字段的参数名中含有度量单位，例如m: 1.76，这些参数名需要保存，确保信息准确
    retain_template_param = (['m', 'end', 'reason', 'award', 'ft', 'in', 'meter', 'meters',
                              'cm'], re.compile(r'\d+'))

    def __init__(self, values, entry):
        """
        :param values: 待解析的字典数据
        :param entry: title，词条名
        """
        # 每个字段含有的props和values
        self._fields = {'template_name': self.template_name,
                        'fields': {
                            k: {'relation_props': v[0], 'values': []} if isinstance(v[0], dict) else {'values': []} for
                            k, v in self.fields_map.items()},
                        'entry': entry}
        # 对待解析的字典数据做字段匹配
        for k, v in values.items():
            field = None
            index = None
            for kk, vv in self.fields_map.items():
                # 字段匹配
                tag, res = _matches(k.lower().strip(), vv)
                if tag:
                    field = kk
                    # 是否包含多值数据，检查下标
                    if res:
                        groups = [int(i) for i in res.groups() if i]
                        if groups:
                            index = groups.pop()
                    break
            if field:
                # 对wiki对象递归解析
                p_v = self.parse(v.strip())
                h_v = ''.join([str(i) for i in p_v]).strip()
                if h_v:
                    _console_log.logger.debug(f'\n{field}: {h_v}\n')
                    if index:
                        h_v = {index: h_v}
                    if h_v not in self._fields['fields'][field]['values']:
                        self._fields['fields'][field]['values'].append(h_v)
        # 多值属性不为空时，将多值属性解析成一一对应
        if self.multi_values_field is not None:
            fields_values = {k: v for k, v in self._fields['fields'].items() if
                             v['values'] and all([k not in kk[-1] for kk in
                                                  self.multi_values_field.values()])}
            multi_values_field = {
                k: {'relation_props': v[0], 'values': []} if isinstance(v[0], dict) else {'values': []} for
                k, v in self.multi_values_field.items()}
            for k, v in self._fields['fields'].items():
                if v['values']:
                    for i_k, i_v in self.multi_values_field.items():
                        i_f = i_v[-1]
                        if k in i_f:
                            for iii, jjj in enumerate(v['values']):
                                if not isinstance(jjj, dict):
                                    v['values'][iii] = {str(0) + str(iii): v['values'][iii]}
                            multi_values_field[i_k]['values'].append({k: v['values']})
            multi_values_field = {k: v for k, v in multi_values_field.items() if v['values']}
            # 为主实体entry增加props, 构建知识图谱时有用
            name = []
            for k, v in multi_values_field.items():
                name.append(
                    f"{k}: ({', '.join([list(i.keys())[0] for i in v['values']])})"
                )
                v['values'] = _get_multi_values(v['values'])
            fields_values.update(multi_values_field)
            if name:
                self._fields['primary_entity_props'] = {'multi_values_field': '\n'.join(name)}

            # 检查不在多值属性要求的字段是否包含多值数据，如果包含超过2个，抛出异常，有1个时会给出警告
            _values = set([j for i in self.multi_values_field.values() for j in i[-1]])
            _multi = []
            for k, v in fields_values.items():
                if k not in _values:
                    if _is_include_dict(v['values']):
                        _multi.append(k)
            if len(_multi) >= 2:
                raise ValueError(f"field({', '.join(_multi)})包含字典即多值数据，不能当成单独字段解析，请将该字段放入multi_values_field中进行解析")
            elif _multi:
                _file_log.logger.warning(f"未指定在multi_values_field中多值字段({_multi[0]})")
                fields_values[_multi[0]]['values'] = [list(i.values())[0] for i in fields_values[_multi[0]]['values']]
        # 多值属性为空时，自动将多值属性解析为一个other info字段
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
                        multi_values_field.append({k: v['values']})
                        name.append(k)
                    else:
                        fields_values[k] = v
            if multi_values_field:
                fields_values.update({'Other Info': {'relation_props': {'zh': '其他信息'},
                                                     'values': _get_multi_values(multi_values_field)}})
                self._fields['primary_entity_props'] = {'multi_values_field': f"Other Info: ({', '.join(name)})"}
        self._fields['fields'] = fields_values

    @classmethod
    def parse(cls, p_t):
        # 递归解析wiki对象
        p_t = mwp.parse(p_t)
        p_t = p_t.filter(recursive=False)
        for i, j in enumerate(p_t):
            if isinstance(j, mwp.wikicode.Template):
                values = []
                for k in j.params:
                    tag, res = _matches(k.name.strip_code().strip(' ').lower(), cls.retain_template_param)
                    res = res.group() if res else ''
                    if tag and not _matches(k.value.strip_code().strip(' ').lower(), cls.discard_template_value)[0]:
                        if _is_int(res):
                            values.append(k.value.strip_code().strip(' '))
                        else:
                            values.append(f"({k.name.strip_code().strip(' ')}: {k.value.strip_code().strip(' ')})")
                if _matches(j.name.strip_code().strip(' ').lower(), cls.retain_template_name)[0]:
                    res = f"({j.name.strip_code().strip(' ')}: {', '.join(values)})"
                else:
                    res = ', '.join(values)
                p_t[i] = mwp.parse(res)
            elif isinstance(j, mwp.wikicode.ExternalLink):
                p_t[i] = j.url
            elif isinstance(j, mwp.wikicode.Tag):
                rs = mwp.parse('\n') if j.tag.strip_code().strip(' ') == 'br' else mwp.parse(
                    j.contents.strip_code().strip(' '))
                p_t[i] = rs
            elif isinstance(j, mwp.wikicode.Wikilink):
                if not _matches(j.title.strip_code().strip(' ').lower(), cls.discard_wikilink_value)[0]:
                    p_t[i] = mwp.parse(j.title.strip_code().strip(' '))
                else:
                    p_t[i] = mwp.parse(None)
            elif isinstance(j, mwp.wikicode.HTMLEntity):
                p_t[i] = mwp.parse(j.normalize())
            elif any([isinstance(j, k) for k in cls.dont_parse_type]):
                p_t[i] = mwp.parse(None)
        if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
            return p_t
        return cls.parse(p_t)

    @property
    def fields(self):
        # 获取字典类型的数据
        return self._fields

    @property
    def graph_entities(self):
        # 获取构建图谱时需要的类三元组数据
        result = []
        fields = self.fields
        t_n = fields['template_name']
        s_e = fields['entry']
        entry_props = fields.get('primary_entity_props', {})
        for k, v in fields['fields'].items():
            relation_attr = v.get('relation_props', {})
            for vl in v['values']:
                result.append((k, vl, relation_attr, entry_props))
        return {'node_label': t_n, 'node_name': s_e, 'node_relation': result}


class TemplateOfficer(TemplateBase):
    template_name = 'Officer'
    fields_map = {
        '_Reign': ({'zh': '君主统治时期/任期/当政期'}, re_compile(r'reign'),),
        '_Successor': ({'zh': '（政党、政府的）接替者/继任者'}, ['heir'], re_compile(r'successor|succeeded|succeeding')),
        '_Predecessor': ({'zh': '（政党、政府的）前任'}, re_compile(r'predecessor|preceded|preceding'),),
        '_Coronation': ({'zh': '加冕礼'}, re_compile(r'coronation'),),
        '_Succession': ({'zh': '继任/继承权（尤指王位的）'}, re_compile(r'succession'),),
        '_Regent': ({'zh': '摄政者'}, re_compile(r'regent'),),
        '_Office': ({'zh': '要职'}, re_compile(r'office.{,2}|order'),),
        '_Prime Minister': ({'zh': '总理/首相'}, re_compile(r'prime.*?minister'),),
        '_Minister': ({'zh': '部长/大臣'}, re_compile(r'minister'),),
        '_Term Start': ({'zh': '（政党、政府的）任期开始时间'}, re_compile(r'term.*?start'),),
        '_Term End': ({'zh': '（政党、政府的）任期结束时间'}, re_compile(r'term.*?end'),),
        '_Term': ({'zh': '（政党、政府的）任期'}, re_compile(r'term'),),
        '_Monarch': ({'zh': '君主/帝王'}, re_compile(r'monarch')),
        '_Majority': ({'zh': '(获胜的)票数/多数票'}, re_compile(r'majority')),
        '_Assembly': ({'zh': '议会'}, re_compile(r'assembly')),
        '_State': ({'zh': '州'}, re_compile(r'state')),
        '_Deputy': ({'zh': '副职'}, re_compile(r'deputy'),),
        '_Leader': ({'zh': '领导'}, re_compile(r'leader'),),
        '_Alongside': ({'zh': '合作/并肩工作'}, re_compile(r'alongside'),),
        '_President': ({'zh': '总统'}, re_compile(r'president'),),
        '_Vice President': ({'zh': '副总统'}, re_compile(r'vice.*?president'),),
        '_Governor': ({'zh': '总督/州长'}, re_compile(r'governor|governor.*?general'),),
        '_Vice Governor': ({'zh': '副总督/副州长'}, re_compile(r'vice.*?governor')),
        '_Appointer': ({'zh': '任命者'}, re_compile(r'appointer'),),
        'Cabinet': ({'zh': '内阁'}, ['cabinet'],),
        'Department': ({'zh': '部门'}, ['department'],),
        'Allegiance': ({'zh': '(对政党、宗教、统治者的)忠诚/效忠'}, re_compile(r'allegiance')),
        '_Nominator': ({'zh': '提名人'}, re_compile(r'nominator'),),
        '_Chancellor': ({'zh': '(德国或奥地利的)总理/(英国的)财政大臣/(英国大学的)名誉校长'}, re_compile(r'chancellor'),),
        '_Lieutenant': ({'zh': '中尉'}, re_compile(r'lieutenant'),),
        '_Appointed': ({'zh': '任职日期'}, re_compile(r'appointed'),),
        'Service Years': ({'zh': '服务年限'}, re_compile(r'service.*?years?')),
        'Rank': ({'zh': '等级/军衔'}, ['rank']),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Office': ({'zh': '重要职务'},
                   ['_Reign', '_Successor', '_Predecessor', '_Coronation', '_Succession', '_Regent', '_Office',
                    '_Prime Minister', '_Minister', '_Term Start', '_Term End', '_Term', '_Monarch', '_Majority',
                    '_Assembly', '_State', '_Deputy', '_Leader', '_Alongside', '_President', '_Vice President',
                    '_Governor', '_Appointer', '_Nominator', '_Chancellor', '_Lieutenant', '_Appointed',
                    '_Vice Governor'])
    }


class TemplateSportsPlayer(TemplateBase):
    template_name = 'Sports Player'
    fields_map = {
        'Player Name': ({'zh': '运动员名称'}, re_compile(r'player.*?name'),),
        'Current Club': ({'zh': '目前俱乐部'}, re_compile(r'current.*?club'),),
        'Club Number': ({'zh': '运动员编号'}, re_compile(r'club.*?number'),),
        'Position': ({'zh': '运动员定位'}, ['position'],),
        '_Years': ({'zh': '服役年份'}, re_compile(r'years?|club.*?years?'),),
        '_Clubs': ({'zh': '服役俱乐部'}, re_compile(r'clubs?'),),
        '_Caps(Goals)': ({'zh': '出场数(进球数)'}, re_compile(r'caps\(goals\)'),),
        '_Caps': ({'zh': '出场数'}, re_compile(r'caps?'),),
        '_Goals': ({'zh': '进球数'}, re_compile(r'goals?'),),
        '_National Years': ({'zh': '国家队服役年份'}, re_compile(r'national.*?years?'),),
        '_National Team': ({'zh': '国家队'}, re_compile(r'national.*?teams?'),),
        '_National Caps(Goals)': ({'zh': '在国家队出场数(在国家队进球数)'}, re_compile(r'national.*?caps\(goals\)'),),
        '_Youth Clubs': ({'zh': '青年俱乐部'}, re_compile(r'youth.*?clubs?'),),
        '_Youth Years': ({'zh': '青年俱乐部服役年份'}, re_compile(r'youth.*?years?'),),
        '_Youth Caps(Goals)': ({'zh': '在青年俱乐部出场数(在青年俱乐部进球数)'}, re_compile(r'youth.*?caps\(goals\)'),),
        '_Youth Caps': ({'zh': '在青年俱乐部出场数'}, re_compile(r'youth.*?caps?'),),
        '_Youth Goals': ({'zh': '在青年俱乐部进球数'}, re_compile(r'youth[-_\s]*goals?'),),
        '_National Caps': ({'zh': '在国家队出场数'}, re_compile(r'national.*?caps?'),),
        '_National Goals': ({'zh': '在国家队进球数'}, re_compile(r'national[-_\s]*goals?'),),
        'Total Caps': ({'zh': '总出场数'}, re_compile(r'total.*?caps?'),),
        'Total Goals': ({'zh': '总进球数'}, re_compile(r'total.*?goals?'),),
        '_Manager Clubs': ({'zh': '管理俱乐部'}, re_compile(r'manager.*?clubs?'),),
        '_Manager Years': ({'zh': '管理俱乐部年份'}, re_compile(r'manager.*?years?'),),
        'Coach': ({'zh': '教练'}, ['coach'],),
        'Medal': ({'zh': '奖牌'}, re_compile(r'medal.*?templates?'),),
        'Competition': ({'zh': '比赛信息'}, re_compile(r'results?', mode='e')),
        'Style': ({'zh': '风格'}, re_compile(r'plays?')),
        'Event': ({'zh': '比赛项目'}, ['event']),
        'Head Coach': ({'zh': '总教练'}, re_compile(r'head.*?coach')),
        'Sports': ({'zh': '运动项目'}, re_compile(r'sports?')),
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


class TemplatePerformanceWorker(TemplateBase):
    template_name = 'Performance Worker'
    fields_map = {
        'Traditional Chinese Name': ({'zh': '繁体名字'}, ['tradchinesename'],),
        'Pinyin Chines Name': ({'zh': '名字拼音'}, ['pinyinchinesename'],),
        'Simplified Chinese Name': ({'zh': '简体名字'}, ['simpchinesename'],),
        'Genre': ({'zh': '体裁/类型（文学、艺术、电影或音乐的）'}, ['genre'],),
        'Label': ({'zh': '唱片公司'}, ['label'],),
        'Instrument': ({'zh': '乐器'}, ['instrument', 'instruments'],),
        'Voice Type': ({'zh': '声音类型'}, re_compile(r'voice.*?type'),),
        'Chinese Name': ({'zh': '中文名'}, re_compile(r'chinese.*?name'),),
        'Notable Role': ({'zh': '著名角色'}, re_compile(r'notable.*?roles?'),),
        'Associated Acts': (
            {'zh': '相关艺术家/相关表演者'}, re_compile(r'associated.*?acts?')),
        'Current Members': ({'zh': '现有成员'}, re_compile(r'current.*?members?'),),
        'Past Members': ({'zh': '过去成员'}, re_compile(r'past.*?members?'),),
        'English Name': ({'zh': '英文名'}, re_compile(r'nama.*?inggeris'),),
        'Location': ({'zh': '表演场地/外景拍摄地'}, ['location']),
        'Dress Size': ({'zh': '服装尺码'}, re_compile(r'dress.*?size'),),
        'Shoe Size': ({'zh': '鞋子尺码'}, re_compile(r'shoe.*?size'),),
        'Number Films': ({'zh': '电影数目'}, re_compile(r'number.*?films'),),
        'Orientation': ({'zh': '性取向'}, ['orientation'],),
        'Films': ({'zh': '电影'}, ['films', 'film'],),
        'Agent': ({'zh': '经纪人'}, ['agent'],),
        'Television': ({'zh': '电视节目'}, ['television'],),
        'Medium': ({'zh': '(传播信息的)媒介'}, ['medium'])
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateResearchers(TemplateBase):
    template_name = 'Researchers'
    fields_map = {
        'Workplace': ({'zh': '工作地'}, re_compile(r'work.*?places?')),
        '_Thesis Year': ({'zh': '论文年份'}, re_compile(r'thesis.*?years?')),
        '_Thesis Title': ({'zh': '论文标题'}, re_compile(r'thesis.*?titles?')),
        '_Thesis Url': ({'zh': '论文链接'}, re_compile(r'thesis.*?urls?')),
        'Fields': ({'zh': '领域'}, ['field', 'fields']),
        'Academic Advisors': ({'zh': '学术顾问'}, re_compile(r'academic.*?advisors?')),
        'Doctoral Advisors': ({'zh': '博士生导师'}, re_compile(r'doctoral.*?advisors?')),
        'Boards': ({'zh': '董事会'}, ['boards']),
        'Doctoral Students': ({'zh': '博士生'}, re_compile(r'doctoral.*?students?')),
        'Notable Students': ({'zh': '著名学生'}, re_compile(r'notable.*?students?')),
        'Contributions': ({'zh': '贡献'}, ['contributions', 'contribution']),
        'Notable Ideas': ({'zh': '著名想法'}, re_compile(r'notable.*?ideas?')),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Thesis': ({'zh': '论文'}, ['_Thesis Title', '_Thesis Year', '_Thesis Url'])
    }