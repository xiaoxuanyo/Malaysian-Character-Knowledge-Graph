# -*- coding: utf-8 -*-
"""
@time   : 2021-2-28 1:57
@author : xiexx
@email  : xiaoxuanemail@163.com
"""

from wiki_person_parser import XMLParser, Parser

if __name__ == '__main__':
    xml_parser = XMLParser(filter_categories=['Orang', 'Tokoh', 'Kelahiran', 'Kematian'], category='Kategori',
                           code='ms')

    xml_parser.parse_file_block('../ms_wiki_data/mswiki-20210401-pages-articles-multistream.xml')
    xml_parser.save('../ms_wiki_data/ms_person_data.json')

    test = "{{Infobox actor\n|name = Normah Damanhuri \n|image = \n|image_size = \n|caption = \n|birth_name = " \
           "\n|birth_date = {{birth date and age|1952|1|1}} \n|birth_place = [[Johor]], [[Persekutuan Tanah Melayu" \
           "]] (kini [[Malaysia]])\n|occupation = Pelakon \n|years_active = 1980-an - kini\n|spouse = \n|children " \
           "= {{plainlist|\n* Ahya Ulumuddin Rosli\n* Liana Rosli\n}}\n|relatives = [[Aripah Damanhuri]] " \
           "(kakak)\n|parents = \n}}"
    print(Parser.parse_wiki_data(test, entry='test'))
