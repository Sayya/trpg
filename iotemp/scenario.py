from basemods import TrpgError
from iotemp import Template
# from trpgmods import Param, Thing, Process, Event, Route, Role

class Scenario:
    root = dict()

    def __init__(self):
        pass
    
    @classmethod
    def open(self, name, group):
        m = list() # DBからの引き込み
        for obj in m:
            t = Template(obj.classt)
            t.jsonload(obj.argjson)
            t.makeobj()
    
    @classmethod
    def dummy(self):
        return (list(), '', False)
            
    @classmethod
    def argdic_first(self, *dummy):
        return {'curr_func': Scenario.group_out, 'arg': (), 'next_func': Scenario.group_in}

    @classmethod
    def group_out(self):
        return (list(Template.holder.keys()), 'グループを指定してください', False)

    @classmethod
    def group_in(self, group):
        Scenario.group = group
        return {'curr_func': Scenario.class_out, 'arg': (), 'next_func': Scenario.class_in}

    @classmethod
    def class_out(self):
        # インポート部分
        from basemods import Holder

        classts = ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role')

        Scenario.candi = [Holder.classt(c) for c in classts]

        return (Scenario.candi, 'クラスを選んでください', True)
        
    @classmethod
    def class_in(self, classt):
        Scenario.classt = classt
        return {'curr_func': Scenario.operation_out, 'arg': (), 'next_func': Scenario.operation_in}

    @classmethod
    def operation_out(self):
        option = {0: 'クラス作成', 1: 'テンプレートマッピング', 2: 'クラスインスタンス一覧'}
        message = '{0} クラス操作を選択します'.format(Scenario.classt.__name__)
        return (option, message, False)

    @classmethod
    def operation_in(self, opted):
        if opted == '0':
            # 0: 'クラス作成' を選択 
            Scenario.template = Template(Scenario.classt, Scenario.group)
        
            return {'curr_func': Scenario.template.dialog_out, 'arg': (), 'next_func': Scenario.template.dialog_in}
            
        elif opted == '1':
            # 1: 'テンプレートマッピング' を選択
            return {'curr_func': Scenario.template_out, 'arg': (), 'next_func': Scenario.template_in}
            
        elif opted == '2':
            # 2: 'クラスインスタンス一覧' を選択
            for v in Scenario.classt.master.values():
                Template.attrdump(v)
            return {'curr_func': Scenario.operation_out, 'arg': (), 'next_func': Scenario.operation_in}

        else:
            raise TrpgError('OK Fully Complete!')

    @classmethod
    def template_out(self):
        print(list(Template.holder.keys()))
        option = Template.holder[Scenario.group][Scenario.classt]
        message = 'グループ -{0}- > クラス -{1}- のテンプレート選択'.format(Scenario.group, Scenario.classt.__name__)
        return (option, message, True)

    @classmethod
    def template_in(self, rtn):
        return Template.holdermap(Scenario.group, Scenario.classt, rtn)

    @classmethod
    def save(self):
        # delete * from scenario where name=#{name}
        # t.jsondumps for all obj
        # insert senario set jsondumps
        pass

    @classmethod
    def close(self):
        pass