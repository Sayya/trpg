from trpg import TrpgError, Master
from inspect import signature, getmembers, isfunction
import trpg
from trpg import Master, TrpgError, Dice, Param, Thing, Process, Event, Route, Role

class Template(Master):
    master = dict()
    pid = 0

    def __init__(self, classt):
        super().__init__(str(Template.pid))
        self.classt = classt

    def dialog(self):
        self.sig = signature(self.classt.__init__).parameters

        if not issubclass(self.classt, Master):
            raise TrpgError('{0} は {1} のサブクラスではありません'.format(self.classt.__name__, Master.__name__))

        print('{0} のセッティング'.format(self.classt.__name__))
    
        argdic = dict()
        for i in list(self.sig)[1:]:
            name = self.sig[i].name
            anno = self.sig[i].annotation
            dvalue = self.sig[i].default
            dclass = type(self.sig[i].default)

            if dclass.__name__ == 'type':
                print('[parameter]{0} (Necessary)'.format(name))
            else:
                print('[parameter]{0} : [default]{1} ({2})'.format(name, dvalue, dclass.__name__))
            
            annos = anno.split(',')
            tmpl = annos[0]
            if len(annos) > 1:
                desc = annos[1]

            def check(tmpl):
                tmpls = tmpl.split('-')
                print(tmpls)

                typet = tmpls[0]
                if len(tmpls) > 2:
                    numbt = tmpls[2]
                    if numbt < 1 and 1000 < numbt:
                        numbt = 1000
                if len(tmpls) > 1:
                    valut = tmpls[1]

                if typet == 'str':
                    rtn = input('{0} >'.format(desc))
                elif typet == 'int':
                    rtn = int(input('{0} >'.format(desc)))
                elif typet == 'bool':
                    rtn = bool(input('{0} >'.format(desc)))
                elif typet == 'tuple':
                    tlis = list()
                    for i in range(int(numbt)):
                        tlis.append(check(valut))
                    rtn = tuple(tlis)
                elif typet == 'list':
                    tlis = list()
                    for i in range(int(numbt)):
                        tlis.append(check(valut))
                    rtn = tlis
                elif typet == 'dict':
                    tt = typet.split(':')
                    tlis = list()
                    for i in range(int(numbt)):
                        keyt = check(tt[0])
                        valt = check(tt[1])
                        tlis.append((keyt, valt))
                    rtn = dict(tlis)
                else:
                    tt = typet.split('.')
                    if tt[0] in ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role'):
                        clst = getattr(trpg, tt[0])
                        if tt[1] == 'name':
                            candi = list(clst.master.keys())
                        elif tt[1] == 'deed':
                            gg = getmembers(clst, isfunction)
                            candi = [g[0] for g in gg]
                        print('IN {0}'.format(candi))
                        rtn = input('{0} >'.format(desc))
                return rtn

            argdic[name] = check(tmpl)

        print('[result]{0}'.format(argdic))
        print()

    def save(self):
        pass
    
    def load(self):
        pass
    
    def makeobj(self):
        try:
            self.classt(**self.argdic)
        except:
            print('{0} の作成に失敗'.format(self.classt.__name__))
        else:
            print('{0} の作成に成功'.format(self.classt.__name__))

    def dumprolething(self):
        pass


