from basemods import TrpgError, Master, Dice
from inspect import signature, getmembers, isfunction
import json
# from trpgmods import Thing, Role

class Template(Master):
    master = dict()
    pid = 0
    holder = dict()
    dice = dict()

    def __init__(self, classt, group='', name=''):
        """ 初期化及びグループの設定 """
        super().__init__(str(Template.pid))
        self.classt = classt
        self.group = group
        self.name = name
        self.existclss = None

        if group not in Template.holder.keys():
            Template.holder[self.group] = {self.classt: dict()}

        if classt not in Template.holder[self.group].keys():
            Template.holder[self.group][self.classt] = dict()

        if name not in Template.holder[self.group][classt].keys():
            Template.holder[self.group][classt][self.name] = ''

    def check_out(self, tmpl, desc, numbt=None):
        # インポート部分
        from basemods import Holder

        def outputu(desc, typet, candi=list()):
            self.default = None
            try:
                if self.existclss is not None:
                    self.default = getattr(self.existclss, self.s_name)
                    message = '{0}({1}): {2} (default: {3})'.format(desc, self.s_name, typet, self.default)
                else:
                    message = '{0}({1}): {2}'.format(desc, self.s_name, typet)

                # (型, 候補リスト, 繰り返し回数, 入力領域, デフォルト)
                return (typet, candi, self.numbt, list(), self.default)
            except TrpgError as e:
                raise e
        
        tmpls = tmpl.split('-')

        self.typet = tmpls[0]
        self.valut = ''
        self.numbt = numbt # tuple 定数a, list 無制限=0, dict 無制限=0の場合
        if len(tmpls) > 1:
            self.numbt = int(tmpls[1])
            if self.numbt < 1 or 1000 < self.numbt:
                self.numbt = 1000
            self.valut = '-'.join(tmpls[2:])

        if self.typet == 'str':
            if self.s_name == 'name':
                if self.name == '':
                    print('UPDATE IN {0}'.format(list(self.classt.master.keys())))
                return outputu(desc, self.typet)
            else:
                return outputu(desc, self.typet)
        elif self.typet == 'int':
            return outputu(desc, self.typet)
        elif self.typet == 'bool':
            return outputu(desc, self.typet)
        elif self.typet == 'tuple':
            return self.check_out(self.valut, desc, self.numbt)
        elif self.typet == 'list':
            return self.check_out(self.valut, desc, self.numbt)
        elif self.typet == 'dict':
            tt = self.valut.split(':')
            tt0 = self.check_out(tt[0], desc, self.numbt)
            tt1 = self.check_out(tt[1], desc, self.numbt)
            return outputu(desc, 'dict', (tt0, tt1))
        else:
            self.tt = self.typet.split('.')
            classtnames = ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role')
            if self.tt[0] in classtnames:
                self.s_classt = Holder.classt(self.tt[0])
                if self.tt[1] == 'name':
                    self.s_candi = list(self.s_classt.master.keys())
                elif self.tt[1] == 'deed':
                    gg = getmembers(self.s_classt, isfunction)
                    self.s_candi = [g[0] for g in gg]

                print('SELECT IN {0}'.format(self.s_candi))

                return outputu(desc, self.typet, self.s_candi)

    def check_in(self, opted):
        # インポート部分
        from basemods import Holder

        def inputu(desc, rtn):
            if self.existclss is not None:
                if rtn == '':
                    if type(self.default) in (int, str, bool):
                        rtn = self.default
                    else:
                        raise TrpgError('デフォルトを設定します')
            return rtn
        
        print('{0}-{1}-{2} is required'.format(self.typet, self.valut, self.numbt))
        exits = ('q', 'exit', 'quit')

        if self.typet == 'str':
            if self.s_name == 'name':
                if self.name != '':
                    rtn = self.name
                else:
                    rtn = opted
                
                # 更新の場合
                if rtn in list(self.classt.master.keys()):
                    self.existclss = self.classt.master[rtn]
            else:
                rtn = opted
        elif self.typet == 'int':
            try:
                rtn = int(opted)
            except ValueError as e:
                if Dice.checkdice(rtn) > 0:
                    print('MESSAGE: ダイス形式で設定')
                    rtn = opted
                else:
                    print('Exception: {0}'.format(e))
                    rtn = 0
        elif self.typet == 'bool':
            rtn = bool(opted)
        elif self.typet == 'tuple':
            self.tlis = list(opted)
            rtn = tuple(self.tlis)
        elif self.typet == 'list':
            self.tlis = list(opted)
            rtn = self.tlis
        elif self.typet == 'dict':
            keyt = opted
            valt = opted
                
            self.tlis.append((keyt, valt))
            rtn = dict(self.tlis)
        else:
            rtn = opted
            if self.tt[1] == 'name' and rtn not in self.s_candi and rtn not in exits:
                t = Template(self.s_classt, self.group, rtn)
                print('グループ -{0}- > クラス -{1}- > テンプレート -{2}- を作成しました'.format(self.group, self.s_classt.__name__, rtn))
                t.holdermap(self.group, self.s_classt, rtn)
                
        if rtn in exits:
            raise TrpgError('OK Complete!')
        
        if self.existclss is not None:
            setattr(self.existclss, self.s_name, rtn)

        return rtn

    
    @classmethod
    def holdermap(self, group, classt, holder):
        if holder in Template.holder[group][classt]:
            print('SELECT IN {0}'.format(list(classt.master.keys())))
            rtn = input('グループ -{0}- > クラス -{1}- > テンプレート -{2}- のマッピング対象選択 >'.format(group, classt.__name__, holder))
            if rtn in classt.master.keys():
                Template.holder[group][classt][holder] = classt.master[rtn].name
        else:
            print('選択しませんでした')

    def dialog_out(self):
        self.sign = signature(self.classt.__init__).parameters

        if not issubclass(self.classt, Master):
            raise TrpgError('{0} は {1} のサブクラスではありません'.format(self.classt.__name__, Master.__name__))

        print('{0} のセッティング'.format(self.classt.__name__))

        self.argdic_candi = dict()

        for i in list(self.sign)[1:]:

            s = self.sign[i]
            self.s_name = s.name
            anno = s.annotation
            dvalue = s.default
            dclass = type(s.default)

            if dclass is type:
                print('[parameter]{0} (Necessary)'.format(self.s_name))
            else:
                print('[parameter]{0} : [default]{1} ({2})'.format(self.s_name, dvalue, dclass.__name__))
            
            annos = anno.split(',')
            tmpl = annos[0]
            if len(annos) > 1:
                desc = annos[1].replace(';', ',')

                self.argdic_candi[self.s_name] = self.check_out(tmpl, desc)
            else:
                raise TrpgError('アノテーションがありません')
        
        return (self.argdic_candi, 'クラスを作成してください', False)

    def dialog_in(self, opted):
        # インポート部分
        from iotemp import Scenario

        self.jsonload(opted)

        for i in list(self.sign)[1:]:

            s = self.sign[i]
            self.s_name = s.name
            anno = s.annotation

            annos = anno.split(',')
            tmpl = annos[0]
            if len(annos) > 1:
                desc = annos[1].replace(';', ',')

                self.argdic_candi[self.s_name] = self.check_out(tmpl, desc)
            else:
                raise TrpgError('アノテーションがありません')

            try:
                self.argdic[self.s_name] = self.check_out(self.argdic[self.s_name], desc)
            except TrpgError as e:
                print('MESSAGE: ', e.value)
                if self.existclss is not None:
                    # デフォルト
                    self.argdic[self.s_name] = getattr(self.existclss, self.s_name)
                else:
                    self.argdic[self.s_name] = ''

            if self.existclss is not None:
                print('アップデート完了: {0}'.format(self.existclss.name))
                Template.attrdump(self.existclss)
            else:
                self.makeobj()

            return {'curr_func': Scenario.operation_out, 'arg': (), 'next_func': Scenario.operation_in}
    
    @classmethod
    def attrdump(self, trpgobj):
        sig = signature(trpgobj.__init__).parameters
        attrs = dict()
        for i in list(sig):
            name = sig[i].name
            attrs[name] = getattr(trpgobj, name)
        print('{0} CREATED: {1}'.format(trpgobj.__class__.__name__, attrs))
    
    def makeobj(self):
        try:
            self.trpgobj = self.classt(**self.argdic)
        except Exception as e:
            print('{0} CREATION FAILED: {1}'.format(self.classt.__name__, e))
        else:
            Template.attrdump(self.trpgobj)

    def make(self, *arglis, **argdic):
        try:
            self.trpgobj = self.classt(*arglis, **argdic)
        except Exception as e:
            print('{0} CREATION FAILED: {1}'.format(self.classt.__name__, e))
        else:
            Template.attrdump(self.trpgobj)
    
    def jsonload(self, argjson):
        self.argdic = json.load(argjson)

    def jsondumps(self):

        # インポート部分
        from basemods import Holder

        def dumprolething():
            if type(self.trpgobj) is Holder.classt('Thing'):
                self.argdic['name'] = self.trpgobj.name
                self.argdic['params'] = self.trpgobj.params
                self.argdic['propts'] = self.trpgobj.propts
            elif type(self.trpgobj) is Holder.classt('Role'):
                self.argdic['name'] = self.trpgobj.name
                self.argdic['propts'] = self.trpgobj.propts
                self.argdic['params'] = self.trpgobj.params
            
        dumprolething()
        return json.dumps(self.argdic)