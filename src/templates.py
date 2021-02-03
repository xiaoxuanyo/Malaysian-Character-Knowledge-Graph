# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 13:42
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import mwparserfromhell as mwp

__all__ = ['Template', 'TemplateEngineer', 'TemplateChineseActorSinger']


def _is_int(ind):
    try:
        int(ind)
        return True
    except ValueError:
        return False


class TemplateEngine:
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
    en2zh_map = {
        'Name': '名字',
        'Nationality': '国籍',
        'Birth Date': '出生日期',
        'Birth Place': '出生地点',
        'Education': '教育',
        'Occupation': '职业',
        'Years Active': '活跃年份',
        'Origin': '源自',
        'Alias': '别名',
        'Website': '网站',
        'Birth Name': '出生名',
        'Height': '身高',
        'Spouse': '伴侣',
        'Parents': '父母'
    }

    _dont = [mwp.wikicode.Argument, mwp.wikicode.Comment, mwp.wikicode.Heading, mwp.wikicode.HTMLEntity]

    def __init__(self, values):
        self.fields = {k: [] for k in self.fields_map.keys()}
        for k, v in values.items():
            field = self._reverse_fields_map.get(k.strip())
            if field:
                p_v = self.parse(v.strip())
                print(field, ': ', ''.join([str(i) for i in p_v]))
                print('\n')
                # print(link)
                # print(template)
                # print(tag)
                # print(o_link)
                # print('\n')
                self.fields[field].append(''.join([str(i) for i in p_v]))
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
            elif any([isinstance(j, k) for k in cls._dont]):
                p_t[i] = mwp.parse(None)
        if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
            return p_t
        return cls.parse(p_t)


class TemplateEngineer(TemplateEngine):
    fields_map = {
        'Discipline': ['discipline'],
        'Institutions': ['institutions'],
        'Practice Name': ['practice_name'],
        'Significant Projects': ['significant_projects'],
        'Significant Awards': ['significant_awards']
    }
    en2zh_map = {
        'Discipline': '工程学科',
        'Institutions': '机构会员',
        'Practice Name': '实用名称',
        'Significant Projects': '主要项目',
        'Significant Awards': '主要奖项'
    }

    fields_map.update(TemplateEngine.fields_map)
    en2zh_map.update(TemplateEngine.en2zh_map)
    _reverse_fields_map = {i: k for k, v in fields_map.items() for i in v}


class TemplateChineseActorSinger(TemplateEngine):
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
    en2zh_map = {
        'Traditional Chinese Name': '繁体名字',
        'Simplified Chinese Name': '简体名字',
        'Pinyin Chines Name': '拼音',
        'Music Type': '音乐类型',
        'Record Company': '唱片公司',
        'Musical Instrument': '乐器',
        'Influenced': '受影响',
        'Awards': '奖项',
        'Associated artists': '相关艺术家',
        'Partner': '伙伴',
        'Voice Type': '声音类型',
        'Chinese Name': '中文名'
    }
    fields_map.update(TemplateEngine.fields_map)
    en2zh_map.update(TemplateEngine.en2zh_map)
    _reverse_fields_map = {i: k for k, v in fields_map.items() for i in v}


class Template(TemplateEngineer):
    _all = [TemplateEngineer, TemplateChineseActorSinger]

    fields_map = {}
    en2zh_map = {}

    for t in _all:
        fields_map.update(t.fields_map)
        en2zh_map.update(t.en2zh_map)
    _reverse_fields_map = {i: k for k, v in fields_map.items() for i in v}


value = {
    "caption": "Santiago Calatrava di hadapan [[Auditorio de Tenerife]].",
    "name": "Santiago Calatrava Valls",
    "nationality": "Sepanyol",
    "birth_date": "{{birth date and age|1951|7|28|df=y}}",
    "birth_place": "[[Valencia, Sepanyol|Valencia]], Sepanyol",
    "education": "Sekolah Seni [[Universiti Valencia|Valencia]] <br>Sekolah Senibina [[Universiti Valencia|Valencia]] <br>[[Institut Teknologi Persekutuan Switzerland]]",
    "discipline": "[[Jurutera struktur]], [[arkitek]], [[pengarca]]",
    "institutions": "[[Institusi Jurutera Struktur]]",
    "practice_name": "Santiago Calatrava",
    "significant_projects": "[[Kompleks Sukan Olimpik Athens]]<br>[[Auditorio de Tenerife]]<br>[[Jambatan Alamillo]]<br>[[ Jambatan Chords]]<br>[[Ciutat de les Arts i les Ciències]]",
    "significant_awards": "[[Pingat Emas AIA]]<br> Pingat Emas [[IStructE]] <br>Anugerah [[Eugene McDermott]]<br>[[Anugerah Putera Asturias]]"
}

tem = Template(value)
print(tem.fields)
