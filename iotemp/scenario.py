from basemods import TrpgError
from iotemp import Template
# from trpgmods import Param, Thing, Process, Event, Route, Role

class Scenario:
    root = dict()

    def __init__(self):
        pass
    
    def open(self, name, group):
        m = list() # DBからの引き込み
        for obj in m:
            t = Template(obj.classt)
            t.jsonload(obj.argjson)
            t.makeobj()

    def wizard(self):

        def classtmake(classts, group):
            """ クラスを選択＆作成 """
            
            # インポート部分
            from basemods import Holder

            while True:
                candi = dict(list(zip( \
                    list(range(len(classts))), \
                    [Holder.classt(c) for c in classts] \
                )))

                candi_disp = dict(list(zip(list(range(len(classts))), classts)))
                print('SELECT IN {0}'.format(candi_disp))
                rtn = input('クラスを選んでください > ')
                if rtn not in [str(i) for i in candi.keys()]:
                    raise TrpgError('OK Fully Complete!')

                print('SELECT IN {0}'.format({0: 'クラス作成', 1: 'テンプレートマッピング', 2: 'クラスインスタンス一覧'}))
                opted = input('{0} クラス操作を選択します > '.format(candi_disp[int(rtn)]))
                if opted == '0':
                    try:
                        t = Template(candi[int(rtn)], group)
                        t.dialog()
                    except TrpgError as e:
                        print(e)
                elif opted == '1':
                    holdermap(candi[int(rtn)], group)
                elif opted == '2':
                    for v in candi[int(rtn)].master.values():
                        Template.attrdump(v)
                else:
                    raise TrpgError('OK Fully Complete!')
    
        def holdermap(classt, group):
            print('SELECT IN {0}'.format(Template.holder[group][classt]))
            rtn = input('グループ -{0}- > クラス -{1}- のテンプレート選択 >'.format(group, classt.__name__))
            Template.holdermap(group, classt, rtn)

        print('UPDATE IN {0}'.format(list(Template.holder.keys())))
        group = input('グループを指定してください > ')

        classts = ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role')
        try:
            classtmake(classts, group)
        except TrpgError as e:
            print(e)


    def save(self):
        # delete * from scenario where name=#{name}
        # t.jsondumps for all obj
        # insert senario set jsondumps
        pass

    def close(self):
        pass