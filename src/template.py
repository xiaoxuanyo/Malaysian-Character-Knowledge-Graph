# -*- coding: utf-8 -*-
"""
@time   : 2021-2-1 10:08
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import mwparserfromhell as mwp
import json

__all__ = ['TemplateEngine', 'FIELDS_MAP', 'EN2MS_MAP', 'EN2ZH_MAP']

FIELDS_MAP = {
    'Name': ['name'],
    'Alias': ['alias', 'nama', 'othernames', 'other_names', 'others name', 'others_name'],
    'Website': ['website', 'url'],
    'Management Company': ['syarikat pengurusan'],
    'Come From': ['origin'],
    'Birth Name': ['birth_name', 'birth name'],
    'Birth Date': ['birth_date', 'born', 'birthdate'],
    'Genre': ['genre'],
    'Instrument': ['instrument', 'instrumen', 'instruments'],
    'Record Company': ['label', 'record label'],
    'Twitter': ['twitter'],
    'Religion': ['religion', 'agama'],
    'Years Active': ['year_active', 'yearsactive', 'years active', 'years_singing', 'years_active'],
    'Brother': ['relatives', 'saudara'],
    'Birth Place': ['birth_place', 'tempat lahir'],
    'Parents': ['parents', 'parent'],
    'Job': ['occupation', 'occupation(s)', 'pekerjaan'],
    'Citizen': ['nationality'],
    'Related Works': ['associated_acts', 'associated acts'],
    'Native Name': ['native_name'],
    'Honorific Prefix': ['honorific_prefix'],
    'Height': ['height'],
    'Honorific Suffix': ['honorific_suffix'],
    'Current Members': ['current_members', 'currentmembers'],
    'Spouse': ['spouse'],
    'Education': ['education'],
    'Weight': ['weight'],
    'Residence': ['residence'],
    'Birth': ['birth'],
    'Partner': ['partner'],
    'Notable Instruments': ['notable_instruments'],
    'Notable Role': ['notable role'],
    'Awards': ['awards'],
    'Agent': ['agent'],
    'Employer': ['employer'],
    'Alma Mater': ['alma_mater'],
    'Known': ['known'],
    'Children': ['children'],
    'Death Date': ['death_date'],
    'Chinese Name': ['chinesename'],
    'Voice Type': ['voice_type', 'voice type'],
    'Background': ['background'],
    'Status': ['status'],
    'Current Team': ['Current team'],
    'Bike Number': ['Bike number'],
    'Discipline': ['discipline'],
    'Significant projects': ['significant_projects'],
    'Institutions': ['institutions'],
    'Significant Awards': ['significant_awards'],
    'Practice Name': ['practice_name']
}


EN2MS_MAP = {
    'Years Active': 'Tahun aktif',
    'Genre': 'Genre',
    'Instrument': 'Instrumen',
    'Nationality': 'Warganegara',
    'Current Team': 'Pasukan kini',
    'Bike Number': 'Nombor motosikal',
    'Website': 'Laman sesawang',
}

EN2ZH_MAP = {
    'Nationality': '国籍',
    'Birth Date': '出生日期',
    'Birth Place': '出生地点',
}


class TemplateEngine:
    fields_map = FIELDS_MAP

    def __init__(self, values):
        self._setattr(values)

    def _setattr(self, values):
        tm_map = {k.strip().lower(): i.strip() for i, j in self.fields_map.items() for k in j}
        for k, v in values.items():
            attr = tm_map.get(k.strip().lower())
            if attr:
                setattr(self, attr, v.strip())

    @property
    def properties(self):
        return self.__dict__


value = {
    "name": "Amylea Azizan",
    "image": "wikimel.jpg",
    "landscape": "<!-- Tulis \"yes\", jika imej kelihatan lebar. Jika tidak, tinggalkan. -->",
    "caption": "Amylea Azizan",
    "background": "solo_singer",
    "native_name_lang": "Bahasa Melayu",
    "alias": "Amylea AF , Amylea OIAM",
    "birth_date": "{{birth date and age|1986|11|26}}",
    "birth_place": "[[Alor Setar]], [[Kedah]]",
    "origin": "{{MAS}}",
    "death_date": "<!-- {{death date and age|YYYY|MM|DD|YYYY|MM|DD}} (tarikh kematian pertama) -->",
    "occupation": "[[Penyanyi]]",
    "instrument": "Vokal",
    "years_active": "<!-- YYYY–YYYY (atau –kini) -->",
    "label": "Seventeen Eleven Music",
    "associated_acts": "[[Kaer Azami]]<br>[[Megat Adzuan]]",
    "website": "<!-- {{URL|contoh.com}} -->"
}

tem = TemplateEngine(value)
print(tem.properties)
