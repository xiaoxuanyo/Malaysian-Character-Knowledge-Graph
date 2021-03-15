# -*- coding: utf-8 -*-
"""
@time   : 2021-2-3 13:42
@author : xiexx
@email  : xiexx@xiaopeng.com
"""

from src.base import (re_compile, TemplateBase, TemplateOfficer, TemplateResearchers,
                      TemplatePerformanceWorker, TemplateSportsPlayer)


class TemplateMotorcycleRider(TemplateBase):
    template_name = 'Motorcycle Rider'
    fields_map = {
        'Current Team': ({'zh': '目前团队'}, re_compile(r'current.*?team'),),
        'Bike Number': ({'zh': '自行车号码'}, re_compile(r'bike.*?number'),)
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateEngineer(TemplateBase):
    template_name = 'Engineer'


class TemplateWarDetainee(TemplateBase):
    template_name = 'War Detainee'
    fields_map = {
        'Arrest Place': ({'zh': '逮捕地点'}, re_compile(r'arrest.*?place|place.*?arrest'),),
        'Arrest Date': ({'zh': '逮捕日期'}, re_compile(r'arrest.*?date|date.*?arrest'),),
        'Arresting Authority': ({'zh': '逮捕机关'}, re_compile(r'arresting.*?authority'),),
        'Detained At': ({'zh': '拘留处'}, re_compile(r'detained.*?at'),),
        'Charge': ({'zh': '指控'}, ['charge'],),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateTwitchStreamer(TemplateBase):
    template_name = 'Twitch Streamer'
    fields_map = {
        'Channel Name': ({'zh': '频道名'}, re_compile(r'channel.*?name')),
        'Followers': ({'zh': '订阅者'}, re_compile(r'followers?')),
        'Views': ({'zh': '观看数'}, re_compile(r'views?'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateAstronaut(TemplateBase):
    template_name = 'Astronaut'
    fields_map = {
        'Mission': ({'zh': '使命'}, ['mission']),
        'Space Time': ({'zh': '时间'}, ['time'], re_compile(r'space.*?time')),
        'Selection': ({'zh': '选拔'}, ['selection']),
        'Rank': ({'zh': '等级/军衔'}, ['rank']),
        '_Eva': ({'zh': '舱外活动'}, re_compile(r'evas?|eva.*?time')),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Eva': ({'zh': '舱外活动'}, ['_Eva'])
    }


class TemplateCelebrity(TemplateBase):
    template_name = 'Celebrity'


class TemplateJournalist(TemplateBase):
    template_name = 'Journalist'


class TemplateFashionDesigner(TemplateBase):
    template_name = 'Fashion Designer'
    fields_map = {
        'Tag': ({'zh': '标签'}, re_compile(r'label.*?name'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateMilitaryPerson(TemplateBase):
    template_name = 'Military Person'
    fields_map = {
        'Office': ({'zh': '重要职务'}, re_compile(r'commands?')),
        'Branch': ({'zh': '分支部门'}, re_compile(r'branch')),
        'Unit': ({'zh': '部队'}, re_compile(r'unit')),
        'Allegiance': ({'zh': '(对政党、宗教、统治者的)忠诚/效忠'}, re_compile(r'allegiance')),
        'Service Years': ({'zh': '服务年限'}, re_compile(r'service.*?years?')),
        'Battles': ({'zh': '战争'}, re_compile(r'battles?')),
        'Rank': ({'zh': '等级/军衔'}, ['rank']),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateArchitect(TemplateBase):
    template_name = 'Architect'
    fields_map = {
        'Buildings': ({'zh': '建筑物'}, re_compile(r'significant.*?buildings?'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateArchbishop(TemplateBase):
    template_name = 'Archbishop'
    fields_map = {
        '_Enthroned': ({'zh': '即位时间'}, ['enthroned']),
        '_Archbishop Of': ({'zh': '大主教'}, re_compile(r'archbishop', mode='s')),
        '_Consecration': ({'zh': '祝胜礼/授职礼'}, ['consecration']),
        'Motto': ({'zh': '座右铭'}, ['motto']),
        '_Ordination': ({'zh': '派立礼/授神职礼'}, ['ordination']),
        '_Consecrated By': ({'zh': '被祝胜/被授职'}, re_compile(r'consecrated', mode='s')),
        '_Ordained By': ({'zh': '被派立/被授神职'}, re_compile(r'ordained', mode='s')),
        '_Successor': ({'zh': '（政党、政府的）接替者/继任者'}, ['heir'], re_compile(r'successor|succeeded|succeeding')),
        '_Predecessor': ({'zh': '（政党、政府的）前任'}, ['pendahulu'], re_compile(r'predecessor|preceded|preceding'),),
        '_Ended': ({'zh': '结束时间'}, ['ended'])
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '重要职务'},
                                     ['_Enthroned', '_Ended', '_Successor', '_Predecessor',
                                      '_Consecration', '_Consecrated By', '_Ordination', '_Ordained By',
                                      '_Archbishop Of'])}


class TemplateFootballOfficial(TemplateBase):
    template_name = 'Football Official'
    fields_map = {
        '_League': ({'zh': '联盟'}, re_compile(r'league'),),
        '_Role': ({'zh': '角色'}, re_compile(r'roles?'),),
        '_Years': ({'zh': '年份'}, re_compile(r'years?'),),
        '_International Years': ({'zh': '国际年份'}, re_compile(r'international.*?years'),),
        '_International League': ({'zh': '国际联盟'}, re_compile(r'confederation'),),
        '_International Role': ({'zh': '国际角色'}, re_compile(r'international.*?roles?'),)
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'League': ({'zh': '联盟'}, ['_League', '_Role', '_Years']),
        'International League': (
            {'zh': '国际联盟'}, ['_International League', '_International Role', '_International Years'])
    }


class TemplateGolfer(TemplateBase):
    template_name = 'Golfer'
    fields_map = {
        '_Years': ({'zh': '获奖年份'}, re_compile(r'years?')),
        'Tour': ({'zh': '巡回比赛'}, re_compile(r'tour', mode='e')),
        'Turned Pro': ({'zh': '成为职业选手'}, re_compile(r'year.*?professional|professional.*?years?')),
        'Wins': ({'zh': '获胜次数'}, re_compile(r'wins?', mode='e')),
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Awards': ({'zh': '奖项'}, ['Awards', '_Years'])
    }


class TemplateBoxer(TemplateBase):
    template_name = 'Boxer'
    fields_map = {
        'Ko': ({'zh': 'ko胜利次数'}, ['ko']),
        'Total': ({'zh': '总次数'}, ['total']),
        'Style': ({'zh': '风格'}, ['style']),
        'Wins': ({'zh': '获胜次数'}, re_compile(r'wins?')),
        'Draws': ({'zh': '平局次数'}, re_compile(r'draws?')),
        'Losses': ({'zh': '失败次数'}, re_compile(r'losses|loss'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateF1Driver(TemplateBase):
    template_name = 'F1 Driver'
    fields_map = {
        '_Car Number': ({'zh': '车号'}, re_compile(r'car.*?number')),
        '_Years': ({'zh': '年份'}, re_compile(r'years?')),
        'Last Win': ({'zh': '最后一次胜利'}, re_compile(r'last.*?win')),
        'Championships': ({'zh': '锦标赛'}, re_compile(r'championships?')),
        'Poles': ({'zh': '极点'}, re_compile(r'poles?')),
        '_Teams': ({'zh': '团队'}, ['team(s)'], re_compile(r'teams?')),
        'First Win': ({'zh': '第一次胜利'}, re_compile(r'first.*?win')),
        'Last Season': ({'zh': '最后一个赛季'}, re_compile(r'last.*?season')),
        'Races': ({'zh': '竞赛信息'}, re_compile(r'races?')),
        'Fastest Laps': ({'zh': '最快圈速'}, re_compile(r'fastest.*?laps?')),
        'Last Race': ({'zh': '最后一场竞赛'}, re_compile(r'last.*?race')),
        'First Race': ({'zh': '第一场竞赛'}, re_compile(r'first.*?race')),
        'Wins': ({'zh': '获胜次数'}, re_compile(r'wins?')),
        'Podiums': ({'zh': '领奖台次数'}, re_compile(r'podiums?')),
        'Points': ({'zh': '点/分'}, re_compile(r'points?')),
        'Last Position': ({'zh': '最后位置'}, re_compile(r'last.*?position'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Teams': ({'zh': '团队'}, ['_Teams', '_Car Number', '_Years'])
    }


class TemplateVideoGamePlayer(TemplateBase):
    template_name = 'Video Game Player'
    fields_map = {
        'Role': ({'zh': '角色/职能/作用'}, re_compile(r'roles?'),),
        '_Years': ({'zh': '年份'}, re_compile(r'years?')),
        '_Teams': ({'zh': '团队'}, re_compile(r'teams?')),
        '_Coach Years': ({'zh': '教练年份'}, re_compile(r'cyears?')),
        '_Coach Teams': ({'zh': '教练团队'}, re_compile(r'cteams?')),
        'League': ({'zh': '联盟'}, re_compile(r'leagues?')),
        'Games': ({'zh': '游戏'}, re_compile(r'games?'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Teams': ({'zh': '团队'}, ['_Teams', '_Years']),
        'Coach Teams': ({'zh': '教练团队'}, ['_Coach Teams', '_Coach Years'])
    }


class TemplateArtist(TemplateBase):
    template_name = 'Artist'
    fields_map = {
        'Training': ({'zh': '训练/培训'}, ['training']),
        'Fields': ({'zh': '领域'}, ['field', 'fields']),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateMartialArtist(TemplateBase):
    template_name = 'Martial Artist'
    fields_map = {
        'Ko': ({'zh': 'ko胜利次数'}, re_compile(r'kowin', mode='e')),
        'Wins': ({'zh': '获胜次数'}, re_compile(r'wins?', mode='e')),
        'Draws': ({'zh': '平局次数'}, re_compile(r'draws?', mode='e')),
        'Losses': ({'zh': '失败次数'}, re_compile(r'loss|losses', mode='e')),
        'Style': ({'zh': '风格'}, ['style']),
        'Weight Class': ({'zh': '重量级'}, re_compile(r'weight.*?class'))
    }
    fields_map.update(TemplateBase.fields_map)


class TemplatePageantTitleholder(TemplateBase):
    template_name = 'Pageant Titleholder'
    fields_map = {
        'Competition': ({'zh': '比赛信息'}, re_compile(r'competitions?', mode='e')),
        'Agent': ({'zh': '经纪人'}, ['agent'],),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateWrestler(TemplateBase):
    template_name = 'Wrestler'
    fields_map = {
        'Trainer': ({'zh': '训练员/助理教练'}, ['trainer']),
        'Debut': ({'zh': '首次亮相'}, ['debut'])
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateChristianLeader(TemplateBase):
    template_name = 'Christian Leader'
    fields_map = {
        '_Enthroned': ({'zh': '即位时间'}, ['enthroned']),
        '_Archbishop Of': ({'zh': '大主教'}, re_compile(r'archbishop', mode='s')),
        '_Consecration': ({'zh': '祝胜礼/授职礼'}, ['consecration']),
        'Motto': ({'zh': '座右铭'}, ['motto']),
        '_Ordination': ({'zh': '派立礼/授神职礼'}, ['ordination']),
        '_Consecrated By': ({'zh': '被祝胜/被授职'}, re_compile(r'consecrated', mode='s')),
        '_Ordained By': ({'zh': '被派立/被授神职'}, re_compile(r'ordained', mode='s')),
        '_Successor': ({'zh': '（政党、政府的）接替者/继任者'}, ['heir'], re_compile(r'successor|succeeded|succeeding')),
        '_Predecessor': ({'zh': '（政党、政府的）前任'}, ['pendahulu'], re_compile(r'predecessor|preceded|preceding'),),
        '_Ended': ({'zh': '结束时间'}, ['ended'], re_compile(r'term.*?end')),
        '_Appointed': ({'zh': '任职日期'}, re_compile(r'appointed'),),
        '_Cardinal': ({'zh': '红衣主教/枢机主教'}, ['cardinal']),
        '_Created Cardinal By': ({'zh': '被创建基数'}, re_compile(r'created.*?cardinal', mode='s'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {'Office': ({'zh': '重要职务'},
                                     ['_Enthroned', '_Ended', '_Successor', '_Predecessor',
                                      '_Consecration', '_Consecrated By', '_Ordination', '_Ordained By',
                                      '_Archbishop Of', '_Cardinal', '_Created Cardinal By', '_Appointed'])}


class TemplateCriminal(TemplateBase):
    template_name = 'Criminal'
    fields_map = {
        'Penalty': ({'zh': '刑罚/处罚'}, ['penalty'], re_compile(r'conviction.*?penalty')),
        'Victims': ({'zh': '受害人'}, re_compile(r'victims?')),
        'Conviction': ({'zh': '定罪'}, ['conviction']),
        'Allegiance': ({'zh': '(对政党、宗教、统治者的)忠诚/效忠'}, re_compile(r'allegiance')),
        'Motive': ({'zh': '动机'}, ['motive']),
        'Charge': ({'zh': '指控'}, ['charge'],),
    }
    fields_map.update(TemplateBase.fields_map)


class TemplateCyclist(TemplateBase):
    template_name = 'Cyclist'
    fields_map = {
        'Role': ({'zh': '角色/职能/作用'}, re_compile(r'roles?'),),
        '_Pro Team': ({'zh': '专业团队'}, re_compile(r'pro.*?teams?')),
        'Medal': ({'zh': '奖牌'}, re_compile(r'medal.*?templates?'),),
        '_Pro Years': ({'zh': '专业团队年份'}, re_compile(r'pro.*?years?')),
        'Current Team': ({'zh': '目前团队'}, re_compile(r'current.*?team'),),
        'Major Wins': ({'zh': '重大胜利'}, re_compile(r'major.*?wins?'))
    }
    fields_map.update(TemplateBase.fields_map)
    multi_values_field = {
        'Pro Team': ({'专业团队'}, ['_Pro Team', '_Pro Years'])
    }


class TemplateRoyalty(TemplateOfficer):
    template_name = 'Royalty'


class TemplateMinister(TemplateOfficer):
    template_name = 'Minister'


class TemplateOfficeholder(TemplateOfficer):
    template_name = 'Officeholder'


class TemplateVicePresident(TemplateOfficer):
    template_name = 'Vice President'


class TemplatePrimeMinister(TemplateOfficer):
    template_name = 'Prime Minister'


class TemplateMP(TemplateOfficer):
    template_name = 'Member of Parliament'


class TemplateGovernor(TemplateOfficer):
    template_name = 'Governor'


class TemplateSenator(TemplateOfficer):
    template_name = 'Senator'


class TemplatePresident(TemplateOfficer):
    template_name = 'President'


class TemplateJudge(TemplateOfficer):
    template_name = 'Judge'


class TemplateAM(TemplateOfficer):
    template_name = 'Assembly Member'


class TemplateMonarch(TemplateOfficer):
    template_name = 'Monarch'


class TemplateCabinetOfficer(TemplateOfficer):
    template_name = 'Cabinet Officer'


class TemplateIndianPolitician(TemplateOfficer):
    template_name = 'Indian Politician'


class TemplatePolitician(TemplateOfficer):
    template_name = 'Politician'
    fields_map = {
        'Unit': ({'zh': '部队'}, re_compile(r'unit')),
        'Branch': ({'zh': '分支部门'}, re_compile(r'branch')),
        'Battles': ({'zh': '战争'}, re_compile(r'battles?')),
    }
    fields_map.update(TemplateOfficer.fields_map)


class TemplateFirstLady(TemplateOfficer):
    template_name = 'First Lady'


class TemplateChineseActorSinger(TemplatePerformanceWorker):
    template_name = 'Chinese Actor And Singer'


class TemplateModel(TemplatePerformanceWorker):
    template_name = 'Model'


class TemplateAdultBiography(TemplatePerformanceWorker):
    template_name = 'Adult Biography'


class TemplateActor(TemplatePerformanceWorker):
    template_name = 'Actor'


class TemplateIndonesiaArtist(TemplatePerformanceWorker):
    template_name = 'Indonesia Artist'


class TemplateComedian(TemplatePerformanceWorker):
    template_name = 'Comedian'


class TemplateMusicalArtist(TemplatePerformanceWorker):
    template_name = 'Musical Artist'


class TemplateScientist(TemplateResearchers):
    template_name = 'Scientist'


class TemplateEconomist(TemplateResearchers):
    template_name = 'Economist'


class TemplatePhilosopher(TemplateResearchers):
    template_name = 'Philosopher'
    fields_map = {
        'Philosophy': ({'zh': '哲学'}, ['region'])
    }
    fields_map.update(TemplateResearchers.fields_map)


class TemplateFootballPlayer(TemplateSportsPlayer):
    template_name = 'Football Player'


class TemplateSwimmer(TemplateSportsPlayer):
    template_name = 'Swimmer'


class TemplateFieldHockeyPlayer(TemplateSportsPlayer):
    template_name = 'Field Hockey Player'


class TemplateTennisPlayer(TemplateSportsPlayer):
    template_name = 'Tennis Player'
    fields_map = {
        'Singles Record': ({'zh': '单打纪录'}, re_compile(r'single.*?record')),
        'Singles Titles': ({'zh': '单打冠军'}, re_compile(r'single.*?titles?')),
        'Highest Singles Ranking': ({'zh': '最高单打排名'}, re_compile(r'highest.*?single.*?ranking')),
        'Current Singles Ranking': ({'zh': '目前单打排名'}, re_compile(r'current.*?single.*?ranking')),
        'Doubles Record': ({'zh': '双打记录'}, re_compile(r'double.*?record')),
        'Doubles Titles': ({'zh': '双打冠军'}, re_compile(r'double.*?titles?')),
        'Highest Doubles Ranking': ({'zh': '最高双打排名'}, re_compile(r'highest.*?double.*?ranking')),
        'Current Doubles Ranking': ({'zh': '目前双打排名'}, re_compile(r'current.*?double.*?ranking')),
        'Mixed Titles': ({'zh': '混打冠军'}, re_compile(r'mixed.*?titles?')),
        'Mixed Record': ({'zh': '混打记录'}, re_compile(r'mixed.*?record')),
        'Turned Pro': ({'zh': '成为职业选手'}, re_compile(r'turned.*?pro')),
        'Career Prize Money': ({'zh': '职业奖金'}, re_compile(r'career.*?prize.*?money')),
    }
    fields_map.update(TemplateSportsPlayer.fields_map)


class TemplateSquashPlayer(TemplateSportsPlayer):
    template_name = 'Squash Player'
    fields_map = {
        'Date Of Current Ranking': (
            {'zh': '目前排名日期'}, re_compile(r'date.*?current.*?ranking|current.*?ranking.*?date')),
        'Date Of Highest Ranking': (
            {'zh': '最高排名日期'}, re_compile(r'highest.*?ranking.*?date|date.*?highest.*?ranking')),
        'Racquet': ({'zh': '球拍'}, ['racquet']),
        'Finals': ({'zh': '决赛'}, ['finals', 'final']),
        'Titles': ({'zh': '冠军'}, ['titles']),
        'Highest Ranking': ({'zh': '最高排名'}, re_compile(r'highest.*?ranking')),
        'Current Ranking': ({'zh': '目前排名'}, re_compile(r'current.*?ranking')),
    }
    fields_map.update(TemplateSportsPlayer.fields_map)


class TemplateSportPerson(TemplateSportsPlayer):
    template_name = 'Sport Person'
    fields_map = {
        'Teams': ({'zh': '团队'}, re_compile(r'teams?')),
        'College Team': ({'zh': '大学团队'}, re_compile(r'college.*?teams?')),
        'Training': ({'zh': '训练/培训'}, ['training']),
    }
    fields_map.update(TemplateSportsPlayer.fields_map)


class TemplateHandballPlayer(TemplateSportsPlayer):
    template_name = 'Handball Player'


class TemplateGymnast(TemplateSportsPlayer):
    template_name = 'Gymnast'


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
    TemplatePhilosopher: ['infobox philosopher', 'infobox_philosopher'],
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
    TemplateSportPerson: ['infobox sportsperson'],
    TemplateArchitect: ['infobox arkitek', 'infobox architect'],
    TemplateArchbishop: ['infobox archbishop'],
    TemplateAM: ['infobox am'],
    TemplateMonarch: ['infobox monarch', 'infobox_monarch'],
    TemplateHandballPlayer: ['infobox handball biography'],
    TemplateArtist: ['infobox artist'],
    TemplateMartialArtist: ['infobox martial artist'],
    TemplateComedian: ['infobox comedian'],
    TemplateCabinetOfficer: ['infobox pegawai kabinet asasp@,', 'infobox us cabinet official'],
    TemplatePageantTitleholder: ['infobox pageant titleholder'],
    TemplateWrestler: ['infobox wrestler', 'infobox professional wrestler'],
    TemplateIndianPolitician: ['infobox indian politician'],
    TemplatePolitician: ['infobox_politician', 'infobox politician'],
    TemplateGymnast: ['infobox gymnast'],
    TemplateFirstLady: ['infobox first lady'],
    TemplateChristianLeader: ['infobox christian leader'],
    TemplateMusicalArtist: ['infobox musical artist', 'infobox musical artist 2', 'infobox musical_artist'],
    TemplateCriminal: ['infobox criminal'],
    TemplateCyclist: ['infobox cyclist']
}

TEMPLATE_MAP = {i: k for k, v in _TEMPLATE_MAP.items() for i in v}

MULTI_DICT = {i.template_name: [] for i in _TEMPLATE_MAP.keys()}

if __name__ == '__main__':
    value = {
        "name": "Adam Derek Scott",
        "image": "[[Imej:Adam_scott.jpg|thumb|right|Adam Scott.]]",
        "date": "July 16",
        "height": "6 [[Feet (unit of length)|ft]] 1 [[inch|in]] (1.85 [[metre|m]])",
        "year": "1980",
        "birth place": "Adelaide, Australia",
        "nationality": "{{AUS}}",
        "residence": "[[Crans sur Sierre]], [[Switzerland]]",
        "college": "University of Nevada, Las Vegas",
        "year professional": "June 2000",
        "current tour": "[[PGA Tour]] (joined 2003),",
        "professional wins": "12 (PGA Tour 5; European Tour 5; other 2)",
        "majorsandyearswon": "None",
        "awardnameandyear": "None"
    }
    tem = TemplateGolfer(value, 'Test')
    print(tem.fields)
    # print(tem.graph_entities)
    # for i in tem.fields['fields']['Office']['values']:
    #     print(i, '\n')
    # print(tem.graph_entities)
