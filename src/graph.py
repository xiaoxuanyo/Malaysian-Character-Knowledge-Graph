#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-02-03 22:45
# @Author   : San
# @Project  : character_knowledge_graph
# @File     : graph.py
# @Software : PyCharm
# @Desc     :


from src.templates import Template
from py2neo import Graph, Node, Relationship

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

tem = Template(value, entry='Jay Chou')
graph = Graph("http://localhost:7474", username="neo4j", password="XXX981110")

for i in tem.graph_tuple:
    print(i)
    node1 = Node('singer', name=i[0])
    node2 = Node('singer', name=i[2])
    graph.create(node1)
    graph.create(node2)
    res = Relationship(node1, i[1], node2)
    graph.create(res)

