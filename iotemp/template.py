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

    def check_out(self, s_name, tmpl, desc):
        # インポート部分
        from basemods import Holder

        def outputu(desc, typet, candi=list(), numbt=None):
            default = None
            try:
                if self.existclss is not None:
                    default = getattr(self.existclss, s_name)
                    # message = '{0}({1}): {2} (default: {3})'.format(desc, s_name, typet, default)

                # (型, 候補リスト, 繰り返し回数, 入力領域, デフォルト)
                return (typet, candi, numbt, list(), default)
            except TrpgError as e:
                raise e
        
        tmpls = tmpl.split('-')

        typet = tmpls[0]
        valut = ''
        numbt = None 
        if len(tmpls) > 1:
            numbt = int(tmpls[1]) # tuple 定数a, list 無制限=0, dict 無制限=0の場合
            if numbt < 1 or 100 < numbt:
                numbt = 100
            valut = '-'.join(tmpls[2:])

        if typet == 'str':
            if s_name == 'name':
                if self.name == '':
                    print('UPDATE IN {0}'.format(list(self.classt.master.keys())))
                return outputu(desc, typet)
            else:
                return outputu(desc, typet)
        elif typet == 'int':
            return outputu(desc, typet)
        elif typet == 'bool':
            return outputu(desc, typet)
        elif typet == 'tuple':
            return outputu(desc, 'tuple', self.check_out(s_name, valut, desc), numbt)
        elif typet == 'list':
            return outputu(desc, 'list', self.check_out(s_name, valut, desc), numbt)
        elif typet == 'dict':
            tt = valut.split(':')
            tt0 = self.check_out(s_name, tt[0], desc)
            tt1 = self.check_out(s_name, tt[1], desc)
            return outputu(desc, 'dict', (tt0, tt1), numbt)
        else:
            tt = typet.split('.')
            classtnames = ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role')
            if tt[0] in classtnames:
                s_classt = Holder.classt(tt[0])
                if tt[1] == 'name':
                    s_candi = list(s_classt.master.keys())
                elif tt[1] == 'deed':
                    gg = getmembers(s_classt, isfunction)
                    s_candi = [g[0] for g in gg]

                print('SELECT IN {0}'.format(s_candi))

                return outputu(desc, typet, s_candi)

    def check_in(self, s_name, tmpl, desc, opted):
        # インポート部分
        from basemods import Holder
        
        tmpls = tmpl.split('-')

        typet = tmpls[0]
        numbt = None 
        if len(tmpls) > 1:
            numbt = int(tmpls[1]) # tuple 定数a, list 無制限=0, dict 無制限=0の場合
            if numbt < 1 or 100 < numbt:
                numbt = 100

        if typet == 'str':
            if s_name == 'name':
                if self.name != '':
                    rtn = self.name
                else:
                    rtn = opted
                
                # 更新の場合
                if rtn in list(self.classt.master.keys()):
                    self.existclss = self.classt.master[rtn]
            else:
                rtn = opted
        elif typet == 'int':
            try:
                rtn = int(opted)
            except ValueError as e:
                if Dice.checkdice(rtn) > 0:
                    print('MESSAGE: ダイス形式で設定')
                    rtn = opted
                else:
                    print('Exception: {0}'.format(e))
                    rtn = 0
        elif typet == 'bool':
            rtn = bool(opted)
        elif typet == 'tuple':
            self.tlis = list(opted)
            rtn = tuple(self.tlis)
        elif typet == 'list':
            self.tlis = list(opted)
            rtn = self.tlis
        elif typet == 'dict':
            keyt = opted
            valt = opted
                
            self.tlis.append((keyt, valt))
            rtn = dict(self.tlis)
        else:
            rtn = opted
            tt = typet.split('.')
            classtnames = ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role')
            if tt[0] in classtnames:
                s_classt = Holder.classt(tt[0])
                if tt[1] == 'name':
                    s_candi = list(s_classt.master.keys())
                elif tt[1] == 'deed':
                    gg = getmembers(s_classt, isfunction)
                    s_candi = [g[0] for g in gg]

                if tt[1] == 'name' and rtn not in s_candi:
                    t = Template(s_classt, self.group, rtn)
                    print('グループ -{0}- > クラス -{1}- > テンプレート -{2}- を作成しました'.format(self.group, s_classt.__name__, rtn))
                    t.holdermap(self.group, s_classt, rtn)
        
        if self.existclss is not None:
            if rtn == '':
                default = getattr(self.existclss, s_name)
                if type(default) in (int, str, bool):
                    rtn = default
                else:
                    raise TrpgError('デフォルトを設定します')

            setattr(self.existclss, s_name, rtn)
    
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
            s_name = s.name
            anno = s.annotation
            dvalue = s.default
            dclass = type(s.default)

            if dclass is type:
                print('[parameter]{0} (Necessary)'.format(s_name))
            else:
                print('[parameter]{0} : [default]{1} ({2})'.format(s_name, dvalue, dclass.__name__))
            
            annos = anno.split(',')
            tmpl = annos[0]
            if len(annos) > 1:
                desc = annos[1].replace(';', ',')

                self.argdic_candi[s_name] = self.check_out(s_name, tmpl, desc)
            else:
                raise TrpgError('アノテーションがありません')
        
        return (self.argdic_candi, 'クラスを作成してください', False)

    def dialog_in(self, opted):
        # インポート部分
        from iotemp import Scenario

        self.jsonload(opted)

        for i in list(self.sign)[1:]:

            s = self.sign[i]
            s_name = s.name
            anno = s.annotation

            annos = anno.split(',')
            tmpl = annos[0]
            if len(annos) > 1:
                desc = annos[1].replace(';', ',')

                try:
                    self.check_in(s_name, tmpl, desc, opted)
                except TrpgError as e:
                    print('MESSAGE: ', e.value)
                    if self.existclss is not None:
                        # デフォルト
                        opted[s_name] = getattr(self.existclss, s_name)
                    else:
                        opted[s_name] = ''
            else:
                raise TrpgError('アノテーションがありません')

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