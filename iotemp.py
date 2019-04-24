from trpg import TrpgError, Master
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

        if self.name != '':
            if group not in Template.holder.keys():
                Template.holder[self.group] = {self.classt: set()}

            if classt not in Template.holder[self.group].keys():
                Template.holder[self.group][self.classt] = set()

            Template.holder[self.group][classt].add(self.name)

    def check(self, tmpl, desc, name):
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
            if name == 'name' and self.name != '':
                rtn = self.name
            else:
                rtn = input('{0}({1}) >'.format(desc, typet))
        elif typet == 'int':
            try:
                rtn = int(input('{0}({1}) >'.format(desc, typet)))
            except ValueError as v:
                print('Exception: {0}'.format(v))
                rtn = 0
        elif typet == 'bool':
            rtn = bool(input('{0}({1}) >'.format(desc, typet)))
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
                print('IN {0}'.format(candi))
                rtn = input('{0}({1}) >'.format(desc, typet))
                if rtn not in candi and rtn not in exits:
                    t = Template(classt, group=self.group, name=rtn)
                    t.makefholder(classt)
                
        if rtn in exits:
            raise TrpgError('OK Complete!')
        
        return rtn
    
    def makefholder(self, classt):
        print('IN {0}'.format(Template.holder[self.group][classt]))
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

            if dclass.__name__ == 'type':
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

        print('[result]{0}'.format(self.argdic))
        self.makeobj()
    
    def makeobj(self):
        try:
            self.trpgobj = self.classt(**self.argdic)
        except Exception as e:
            print('{0} の作成に失敗: {1}'.format(self.classt.__name__, e))
        else:
            print('{0} の作成に成功'.format(self.classt.__name__))
    
    def jsonload(self, argjson):
        self.argdic = json.load(argjson)

    def jsondumps(self):

        def dumprolething():
            if type(self.trpgobj) == Thing:
                self.argdic['name'] = self.trpgobj.name
                self.argdic['params'] = self.trpgobj.params
                self.argdic['propts'] = self.trpgobj.propts
            elif type(self.trpgobj) == Role:
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
            for i in range(100):
                exits = ('q', 'exit', 'quit')
                print('Exit IN {0}'.format(exits))
                rtn = input('{0} の作成をします > '.format(classt.__name__))
                if rtn in exits:
                    raise TrpgError('OK Complete!')

                t = Template(classt)
                t.dialog()

        def clsstmake(classts):
            for classt in classts:
                try:
                    tmpltmake(classt)
                except TrpgError as e:
                    print(e)
                
                exits = ('q', 'exit', 'quit')
                print('Exit IN {0}'.format(exits))
                rtn = input('次のクラスの作成します > ')
                if rtn in exits:
                    raise TrpgError('OK Fully Complete!')

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
