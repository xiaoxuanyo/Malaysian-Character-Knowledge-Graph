# Malaysian-Character-Knowledge-Graph
Automatically build Malaysian character knowledge graph

目前对于不同语言，只需修改gen.py生成键值对格式的Infobox(具体名称与对应语言有关)的ps.json数据，
然后修改info.py生成每个Infobox(具体名称与对应语言有关)对应所有字段的result.json数据，
最后对着ps.json与result.json数据即可编写templates.py解析获取自定义的字段。

