from inspect import signature, getmembers, isfunction
import json
import trpg
from trpg import Master, TrpgError, Param, Thing, Process, Event, Route, Role

class Template(Master):
    master = dict()
    pid = 0
    holder = dict()

    def __init__(self, classt, group='', name=''):
        """ 初期化及びグループの設定 """
        super().__init__(str(Template.pid))
        self.classt = classt
        self.name = name
        self.group = group
        self.existclss = None

        if self.name != '':
            if group not in Template.holder.keys():
                Template.holder[self.group] = {self.classt: set()}

            if classt not in Template.holder[self.group].keys():
                Template.holder[self.group][self.classt] = set()

            Template.holder[self.group][classt].add(self.name)

    def check(self, tmpl, desc, name):

        def inputu(desc, typet, name):
            if self.existclss is not None:
                default = getattr(self.existclss, name)
                rtn = input('{0}({1}): {2} (default: {3}) >'.format(desc, name, typet, default))
                if rtn == '':
                    if type(default) in (int, str, bool):
                        rtn = default
                    else:
                        print('デフォルトを設定します')
                        rtn = 'q'
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
                rtn = inputu(desc, typet, name)
        elif typet == 'int':
            try:
                rtn = int(inputu(desc, typet, name))
            except ValueError as v:
                print('Exception: {0}'.format(v))
                rtn = 0
        elif typet == 'bool':
            rtn = bool(inputu(desc, typet, name))
        elif typet == 'tuple':
            tlis = list()
            for i in range(int(numbt)):
                try:
                    tlis.append(self.check(valut, desc, name))
                except TrpgError as e:
                    print('MESSAGE:', e.value)
                    break

            rtn = tuple(tlis)
        elif typet == 'list':
            tlis = list()
            for i in range(int(numbt)):
                try:
                    tlis.append(self.check(valut, desc, name))
                except TrpgError as e:
                    print('MESSAGE:', e.value)
                    break

            rtn = tlis
        elif typet == 'dict':
            tt = valut.split(':')
            tlis = list()
            for i in range(int(numbt)):
                try:
                    keyt = self.check(tt[0], desc, name)
                    valt = self.check(tt[1], desc, name)
                except TrpgError as e:
                    print('MESSAGE:', e.value)
                    break
                
                tlis.append((keyt, valt))
            rtn = dict(tlis)
        else:
            tt = typet.split('.')
            classtnames = ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role')
            if tt[0] in classtnames:
                classt = getattr(trpg, tt[0])
                if tt[1] == 'name':
                    candi = list(classt.master.keys())
                elif tt[1] == 'deed':
                    gg = getmembers(classt, isfunction)
                    candi = [g[0] for g in gg]

                print('SELECT IN {0}'.format(candi))
                rtn = inputu(desc, typet, name)
                if rtn not in candi and rtn not in exits:
                    t = Template(classt, group=self.group, name=rtn)
                    t.makefholder(classt)
                
        if rtn in exits:
            raise TrpgError('OK Complete!')
        
        return setrtn(name, rtn)
    
    def makefholder(self, classt):
        print('SELECT IN {0}'.format(Template.holder[self.group][classt]))
        rtn = input('テンプレート({0}) >'.format(classt.__name__))
        if rtn in Template.holder[self.group][classt]:
            self.dialog()

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
                print('MESSAGE:', e.value)
                self.argdic[name] = ''

        if self.existclss is not None:
            print('アップデート完了: {0}'.format(self.existclss.name))
            self.attrdump(self.existclss)
        else:
            self.makeobj()
        
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
            self.attrdump(self.trpgobj)
    
    def jsonload(self, argjson):
        self.argdic = json.load(argjson)

    def jsondumps(self):

        def dumprolething():
            if type(self.trpgobj) is Thing:
                self.argdic['name'] = self.trpgobj.name
                self.argdic['params'] = self.trpgobj.params
                self.argdic['propts'] = self.trpgobj.propts
            elif type(self.trpgobj) is Role:
                self.argdic['name'] = self.trpgobj.name
                self.argdic['propts'] = self.trpgobj.propts
                self.argdic['params'] = self.trpgobj.params
            
        dumprolething()
        return json.dumps(self.argdic)

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

    def wizard(self, group):
                
        def tmpltmake(classt):
            exits = ('q', 'exit', 'quit')
            print('Exit IN {0}'.format(exits))
            rtn = input('{0} の作成をします > '.format(classt.__name__))
            if rtn in exits:
                raise TrpgError('OK Complete!')

            t = Template(classt)
            t.dialog()

        def clsstmake(classts):
            while True:
                candi = dict(list(zip(list(range(len(classts))), classts)))
                candi_disp = dict(list(zip(list(range(len(classts))), [c.__name__ for c in classts])))
                print('SELECT IN {0}'.format(candi_disp))
                rtn = input('クラスを選んでください > ')
                if rtn not in [str(i) for i in candi.keys()]:
                    raise TrpgError('OK Fully Complete!')

                try:
                    tmpltmake(candi[int(rtn)])
                except TrpgError as e:
                    print(e)

        classts = [Param, Thing, Process, Event, Route, Role]
        try:
            clsstmake(classts)
        except TrpgError as e:
            print(e)


    def save(self):
        # delete * from scenario where name=#{name}
        # t.jsondumps for all obj
        # insert senario set jsondumps
        pass

    def close(self):
        pass
