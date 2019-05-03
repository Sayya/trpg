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
        self.name = name
        self.group = group
        self.existclss = None

        if self.name != '':
            if group not in Template.holder.keys():
                Template.holder[self.group] = {self.classt: dict()}

            if classt not in Template.holder[self.group].keys():
                Template.holder[self.group][self.classt] = dict()

            Template.holder[self.group][classt][self.name] = ''

    def check(self, tmpl, desc, name):
        # インポート部分
        from basemods import Holder

        def inputu(desc, typet, name):
            if self.existclss is not None:
                default = getattr(self.existclss, name)
                rtn = input('{0}({1}): {2} (default: {3}) >'.format(desc, name, typet, default))
                if rtn == '':
                    if type(default) in (int, str, bool):
                        rtn = default
                    else:
                        raise TrpgError('デフォルトを設定します')
            else:
                rtn = input('{0}({1}): {2} >'.format(desc, name, typet))

            return rtn
        
        def setrtn(name, rtn):
            if self.existclss is not None:
                setattr(self.existclss, name, rtn)

            return rtn
        
        tmpls = tmpl.split('-')
        typet = tmpls[0]
        valut = ''
        numbt = ''
        if len(tmpls) > 1:
            numbt = int(tmpls[1])
            if numbt < 1 or 1000 < numbt:
                numbt = 1000
            valut = '-'.join(tmpls[2:])

        # print('{0}-{1}-{2} is required'.format(typet,valut,numbt))
        exits = ('q', 'exit', 'quit')

        if typet == 'str':
            if name == 'name':
                if self.name != '':
                    rtn = self.name
                else:
                    print('UPDATE IN {0}'.format(list(self.classt.master.keys())))
                    rtn = inputu(desc, typet, name)
                
                # 更新の場合
                if rtn in list(self.classt.master.keys()):
                    self.existclss = self.classt.master[rtn]
            else:
                try:
                    rtn = inputu(desc, typet, name)
                except TrpgError as e:
                    raise e
        elif typet == 'int':
            try:
                rtn_str = inputu(desc, typet, name)
            except TrpgError as e:
                raise e

            try:
                rtn = int(rtn_str)
            except ValueError as e:
                if Dice.checkdice(rtn_str) > 0:
                    print('MESSAGE: ダイス形式で設定')
                    rtn = rtn_str
                else:
                    print('Exception: {0}'.format(e))
                    rtn = 0
        elif typet == 'bool':
            try:
                rtn = bool(inputu(desc, typet, name))
            except TrpgError as e:
                raise e
        elif typet == 'tuple':
            tlis = list()
            for i in range(int(numbt)):
                try:
                    tlis.append(self.check(valut, desc, name))
                except TrpgError as e:
                    raise e

            rtn = tuple(tlis)
        elif typet == 'list':
            tlis = list()
            for i in range(int(numbt)):
                try:
                    tlis.append(self.check(valut, desc, name))
                except TrpgError as e:
                    raise e

            rtn = tlis
        elif typet == 'dict':
            tt = valut.split(':')
            tlis = list()
            for i in range(int(numbt)):
                try:
                    keyt = self.check(tt[0], desc, name)
                    valt = self.check(tt[1], desc, name)
                except TrpgError as e:
                    raise e
                
                tlis.append((keyt, valt))
            rtn = dict(tlis)
        else:
            tt = typet.split('.')
            classtnames = ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role')
            if tt[0] in classtnames:
                classt = Holder.classt(tt[0])
                if tt[1] == 'name':
                    candi = list(classt.master.keys())
                elif tt[1] == 'deed':
                    gg = getmembers(classt, isfunction)
                    candi = [g[0] for g in gg]

                print('SELECT IN {0}'.format(candi))

                try:
                    rtn = inputu(desc, typet, name)
                except TrpgError as e:
                    raise e
                
                if tt[1] == 'name' and rtn not in candi and rtn not in exits:
                    t = Template(classt, self.group, rtn)
                    print('グループ -{0}- > クラス -{1}- > テンプレート -{2}- を作成しました >'.format(self.group, classt.__name__, rtn))
                    t.holdermap(self.group, classt, rtn)
                
        if rtn in exits:
            raise TrpgError('OK Complete!')
        
        return setrtn(name, rtn)
    
    @classmethod
    def holdermap(self, group, classt, holder):
        if holder in Template.holder[group][classt]:
            print('SELECT IN {0}'.format(list(classt.master.keys())))
            rtn = input('グループ -{0}- > クラス -{1}- > テンプレート -{2}- のマッピング対象選択 >'.format(group, classt.__name__, holder))
            if rtn in classt.master.keys():
                Template.holder[group][classt][holder] = classt.master[rtn].name
        else:
            print('選択しませんでした')

    def dialog(self):
        sig = signature(self.classt.__init__).parameters

        if not issubclass(self.classt, Master):
            raise TrpgError('{0} は {1} のサブクラスではありません'.format(self.classt.__name__, Master.__name__))

        print('{0} のセッティング'.format(self.classt.__name__))
    
        self.argdic = dict()
        for i in list(sig)[1:]:
            name = sig[i].name
            anno = sig[i].annotation
            dvalue = sig[i].default
            dclass = type(sig[i].default)

            if dclass is type:
                print('[parameter]{0} (Necessary)'.format(name))
            else:
                print('[parameter]{0} : [default]{1} ({2})'.format(name, dvalue, dclass.__name__))
            
            annos = anno.split(',')
            tmpl = annos[0]
            if len(annos) > 1:
                desc = annos[1].replace(';', ',')

            try:
                self.argdic[name] = self.check(tmpl, desc, name)
            except TrpgError as e:
                print('MESSAGE: ', e.value)
                if self.existclss is not None:
                    # デフォルト
                    self.argdic[name] = getattr(self.existclss, name)
                else:
                    self.argdic[name] = ''

        if self.existclss is not None:
            print('アップデート完了: {0}'.format(self.existclss.name))
            Template.attrdump(self.existclss)
        else:
            self.makeobj()
    
    @classmethod
    def attrdump(self, trpgobj):
        sig = signature(trpgobj.__init__).parameters
        attrs = dict()
        for i in list(sig):
            name = sig[i].name
            attrs[name] = getattr(trpgobj, name)
        print('[result]{0}'.format(attrs))
    
    def makeobj(self):
        try:
            self.trpgobj = self.classt(**self.argdic)
        except Exception as e:
            print('{0} の作成に失敗: {1}'.format(self.classt.__name__, e))
        else:
            print('{0} の作成に成功'.format(self.classt.__name__))
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