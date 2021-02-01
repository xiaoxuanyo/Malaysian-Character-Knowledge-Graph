# -*- coding: utf-8 -*-
"""
@time   : 2021-2-1 10:08
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

import mwparserfromhell as mwp
import json

__all__ = ['TemplateEngine', 'FIELDS_MAP']

FIELDS_MAP = {
    'name': ['name'],
    'alias': ['alias', 'nama', 'othernames', 'other_names', 'others name', 'others_name'],
    'website': ['website', 'url'],
    'management company': ['syarikat pengurusan'],
    'come from': ['origin'],
    'birth name': ['birth_name', 'birth name'],
    'birth date': ['birth_date', 'born', 'birthdate'],
    'genre': ['genre'],
    'instrument': ['instrument', 'instrumen', 'instruments'],
    'record company': ['label', 'record label'],
    'twitter': ['twitter'],
    'religion': ['religion', 'agama'],
    'years active': ['year_active', 'yearsactive', 'years active', 'years_singing', 'years_active'],
    'brother': ['relatives', 'saudara'],
    'birth place': ['birth_place', 'tempat lahir'],
    'parents': ['parents', 'parent'],
    'job': ['occupation', 'occupation(s)', 'pekerjaan'],
    'citizen': ['nationality'],
    'related works': ['associated_acts', 'associated acts'],
    'native name': ['native_name'],
    'honorific prefix': ['honorific_prefix'],
    'height': ['height'],
    'honorific suffix': ['honorific_suffix'],
    'current members': ['current_members', 'currentmembers'],
    'spouse': ['spouse'],
    'education': ['education'],
    'weight': ['weight'],
    'residence': ['residence'],
    'birth': ['birth'],
    'partner': ['partner'],
    'notable instruments': ['notable_instruments'],
    'notable role': ['notable role'],
    'awards': ['awards'],
    'agent': ['agent'],
    'employer': ['employer'],
    'alma mater': ['alma_mater'],
    'known': ['known'],
    'children': ['children'],
    'death date': ['death_date'],
    'chinese name': ['chinesename'],
    'voice type': ['voice_type', 'voice type'],
    'background': ['background'],
    'status': ['status'],
    'current team': ['Current team'],
    'bike number': ['Bike number'],
    'discipline': ['discipline'],
    'significant projects': ['significant_projects'],
    'institutions': ['institutions'],
    'significant awards': ['significant_awards'],
    'practice name': ['practice_name']
}


class TemplateEngine:
    fields_map = FIELDS_MAP

    def __init__(self, **kwargs):
        self._setattr(**kwargs)

    def _setattr(self, **kwargs):
        tm_map = {k.strip().lower(): i.strip().lower() for i, j in self.fields_map.items() for k in j}
        for k, v in kwargs.items():
            attr = tm_map.get(k.strip().lower())
            if attr:
                setattr(self, attr, v.strip())
