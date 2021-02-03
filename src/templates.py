# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 13:42
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import mwparserfromhell as mwp

__all__ = ['Template', 'TemplateEngineer', 'TemplateChineseActorSinger']


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

    def __init__(self, values):
        self.fields = {k: [] for k in self.fields_map.keys()}
        for k, v in values.items():
            field = self._reverse_fields_map.get(k.strip())
            if field:
                p_v = mwp.parse(v.strip())
                # text = p_v.filter_text()
                # link = p_v.filter_wikilinks(recursive=False)
                # template = p_v.filter_templates(recursive=False)
                # tag = p_v.filter_tags(recursive=False)
                # o_link = p_v.filter_external_links(recursive=False)
                # print([[j for j in i.split(',') if j.strip()] for i in text])

                t = p_v.filter(recursive=False)
                print(t)
                print([type(ii) for ii in t])
                print('\n')
                # print(link)
                # print(template)
                # print(tag)
                # print(o_link)
                # print('\n')
                self.fields[field].append(p_v)
        self.fields = {k: v for k, v in self.fields.items() if v}


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
    "name": "Jay Chou",
    "image": "Jay Chou in Seoul.jpg",
    "caption": "Jay Chou di tayangan perdana \"[[Secret (filem 2007)|Secret]]\" di [[Seoul]], [[Korea Selatan]], [[10 Januari]] [[2008]]",
    "tradchinesename": "周杰倫",
    "pinyinchinesename": "Zhōu Jiélún",
    "birthdate": "{{birth date and age|1979|01|18}}",
    "birthplace": "[[Linkou]], [[Kaunti Taipei]], [[Taiwan]], [[Republik China]]",
    "othername": "President Chou (周董)",
    "origin": "[[Republik China]] ([[Taiwan]])",
    "height": "173cm",
    "occupation": "[[Penyanyi]], [[pemuzik]], [[komposer]], [[penerbit rakaman]], [[rapper]], [[pengarah filem]], dan [[pelakon]]",
    "genre": "[[Mandopop]], [[R&B]], [[hip hop]], [[pop rap]], [[C-pop]],[[Rock music|rock]]",
    "instrument": "[[Piano]], [[Cello]], [[Guitar]], [[Dram]], [[Guzheng]], [[Harmonika]], [[Violin]],[[Erhu]], [[Pipa]], [[gitar bass]], [[gitar elektrik]]",
    "label": "[[Sony BMG|Sony BMG Asia]], Alfa Music, [[JVR Music]]",
    "yearsactive": "2000–kini",
    "influenced": "[[Nan Quan Mama]]",
    "website": "[http://www.jay2u.com/ jay2u.com]<br />[http://www.jvrmusic.com/artist/artist-index.asp?id=jay jvrmusic.com]",
    "hongkongfilmwards": "'''Pelakon Baru Terbaik'''<br />2006 ''[[Initial D (filem)|Initial D]]''<br />'''Lagu Filem Asli Terbaik'''<br />2007 \"Chrysanthemum Terrace\" (''[[Curse of the Golden Flower]]'')",
    "goldenhorseawards": "'''Pelakon Baru Terbaik'''<br />2005 ''[[Initial D (filem)|Initial D]]''<br />'''Filem Taiwan Paling Cemerlang'''<br />2007 ''[[Secret (filem 2007)|Secret]]''<br />'''Lagu Asli Terbaik'''<br />2007 \"The Secret That Cannot Be Told\" (''[[Secret (filem 2007)|Secret]]'')",
    "mtvasiaawards": "'''Artis Kegemaran, Taiwan'''<br />2002, 2005",
    "goldenmelodyawards": "'''Album Mandarin Terbaik'''<br />2001 ''[[Jay (album)|Jay]]''<br />2002 ''[[Fantasy (album Jay Chou)|Fantasy]]''<br />2004 ''[[Ye Hui Mei (album)|Ye Hui Mei]]''<br />'''Lagu Terbaik'''<br />2008 ''\"Blue and White Porcelein\"'' (''[[On The Run (album Jay Chou)|On The Run]]'')<br />'''Komposer Terbaik'''<br />2002 ''\"Love Before A.D.\"'' (''[[Fantasy (album Jay Chou)|Fantasy]]'')<ref>{{zh icon}} [[Pejabat Penerangan Kerajaan]] ([[Republik China|R.O.C.]]) [http://info.gio.gov.tw/ct.asp?xItem=13498&ctNode=1220&mp=1 Winners of the 13th Golden Melody Awards]. 28 April 2004. Dicapai pada 11 Disember 2007.</ref><br />2008 ''\"Blue and White Porcelein\"'' (''[[On The Run (album Jay Chou)|On The Run]]'')<br />'''Penerbit Terbaik'''<br />2002 ''[[Fantasy (album Jay Chou)|Fantasy]]''\n'''Penerbit Single Terbaik'''<br />2007 ''[[Fearless (filem 2006)|Fearless]] EP''<br />'''Komposer Terbaik (Kategori Instrumen)'''<br />2008 ''\"Piano Room\"'' (''[[Secret (filem 2007)|Secret]]'')<br />'''Penerbit Terbaik (Kategori Instrumen)'''<br />2008 ''Secret Original Movie Soundtrack'' (''[[Secret (filem 2007)|Secret]]'')",
    "awards": "'''[[World Music Awards]]'''<br />Artis Cina Terlaris<br />2004, 2006, 2007"
}

tem = Template(value)
print(tem.fields)

t2 = "[http://www.jay2u.com/ jay2u.com]<br />[http://www.jvrmusic.com/artist/artist-index.asp?id=jay jvrmusic.com]"


def parse(p_t):
    p_t = p_t.filter(recursive=False)
    for i, j in enumerate(p_t):
        if isinstance(j, mwp.wikicode.Template):
            values = [str(k.value) for k in j.params]
            p_t[i] = mwp.parse('-'.join(values))
        elif isinstance(j, mwp.wikicode.ExternalLink):
            p_t[i] = j.url
        elif isinstance(j, mwp.wikicode.Tag):
            p_t[i] = j.contents
        elif isinstance(j, mwp.wikicode.Wikilink):
            p_t[i] = j.text if j.text else j.title
        elif isinstance(j, mwp.wikicode.Argument) or isinstance(j, mwp.wikicode.Comment) or isinstance(j,
                                                                                                       mwp.wikicode.Heading) or isinstance(
            j, mwp.wikicode.HTMLEntity):
            p_t[i] = mwp.parse(None)
    if all([isinstance(ii, mwp.wikicode.Text) for ii in p_t]):
        return p_t
    return parse(mwp.parse(p_t))


print(parse(mwp.parse(t2)))
