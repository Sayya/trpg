from basemods import TrpgError, Master, Arbit
# from trpgmods import Thing, Route

class Role(Master):
    """ 権限の単位、TRPGにおけるPL、PCのPLにあたる """
    master = dict()
    pid = 0

    def __init__(self, \
        name:'str,名前', \
        propts:'list-0-Thing.name,選択肢'=list(), \
        routes:'list-0-Route.name,選択ルート'=list(), \
        group:'str,グループ'=''):

        super().__init__(name)
        self.propts = propts # [Thing().name]
        self.routes = routes # [Route().name]
        self.group = group
        
        self.attrbuild()

    def attrbuild(self):
        # インポート部分
        from basemods import Holder

        self.thing = Holder.master('Thing', '')
        self.items = list()
        self.ordered = dict([('sbj', dict()), ('obj', dict())])

        #Event.focus()で使用
        if len(self.propts) > 0:
            self.sbj = self.getpropts()[0]
            self.obj = self.getpropts()[0]
        else:
            self.sbj = Holder.master('Thing', '')
            self.obj = Holder.master('Thing', '')
        
    def buildvalid(self):
        # インポート部分
        from basemods import Holder
        from iotemp import Template
        
        for v in self.propts:
            # Thing.name のテンプレート処理 - list編
            if v not in Holder.master('Thing').keys():
                idx = self.propts.index(v)
                del self.propts[idx]
                try:
                    tname = Template.holder[self.group][Holder.classt('Thing')][v]
                    self.propts.insert(idx, tname)
                except Exception:
                    print('TEMPLATEERROR: Role.propts -{0}-'.format(self.name))

        for v in self.routes:
            # Route.name のテンプレート処理 - list編
            if v not in Holder.master('Route').keys():
                idx = self.routes.index(v)
                del self.routes[idx]
                try:
                    tname = Template.holder[self.group][Holder.classt('Route')][v]
                    self.routes.insert(idx, tname)
                except Exception:
                    print('TEMPLATEERROR: Role.routes -{0}- v={1}, idx={2}'.format(self.name, v, idx))
    
    def getpropts(self):
        # インポート部分
        from basemods import Holder
        
        return [Holder.master('Thing', i) for i in self.propts]
    
    def getroutes(self):
        # インポート部分
        from basemods import Holder
        
        rtn = list()
        for i in self.routes:
            if i in Holder.master('Route').keys():
                rtn.append(Holder.master('Route', i))
            elif type(i).__name__ in ('function', 'method'):
                rtn.append(i)
        return rtn

    def action(self):
        # インポート部分
        from basemods import Holder
        
        def focus():
            try:
                self.thing = Arbit.inputa(self.getpropts(), self.name, 'thing')
            except TrpgError as e:
                raise e
            
            self.items.clear
            try:
                while Arbit.inpute():
                    self.items.append(Arbit.inputa(self.thing.getpropts(), self.name, 'propts'))
            except TrpgError as e:
                raise TrpgError('Thing -{0}- は他の Thing を所有していません'.format(self.thing.name))

        def on ():
            """ 比較リストに追加（Equip） """
            focus()

            # 検証
            for i in self.items:
                for j in self.thing.getpropts():
                    # 比較リストに追加
                    if i == j:
                        self.thing.f_compare.append(j)
                        self.thing.propts.remove(j.name)

        def off():
            """ 比較リストから削除（UnEquip） """
            focus()

            # 検証
            for i in self.items:
                for j in self.thing.f_compare:
                    # アイテムリストに追加
                    if i == j:
                        self.thing.propts.append(j.name)
                        self.thing.f_compare.remove(j)

        def choice():
            """ 交換リストを更新 """
            focus()

            # 元のアイテムリストに戻す
            self.thing.propts.extend([i.name for i in self.thing.f_xchange])
            self.thing.f_xchange.clear()

            # 検証
            for i in self.items:
                for j in self.thing.getpropts():
                    # 交換リストに代入
                    if i == j:
                        self.thing.f_xchange.append(j)
                        self.thing.propts.remove(j.name)
        
        def way(route):
                endflg = True
                index = self.routes.index(route.name)
                while endflg:
                    endflg = route.noend
                    route.occur(self)
                    route = route.next
                self.routes[index] = route.name
                self.ordered = dict([('sbj', dict()), ('obj', dict())])
        
        actlis = [on, off, choice]
        actlis.extend(self.getroutes())
        try:
            act = Arbit.inputa(actlis, self.name, 'action')
            if type(act) is Holder.classt('Route'):
                way(act)
            else:
                act()
        except TrpgError as e:
            print('MESSAGE: ', e.value)
        
    def order(self, param):
        """ Generator """
        self.propts = [i.name for i in sorted(self.getpropts(), key=lambda x: x.point(param))]
        self.propts.reverse()
        print('ORDER IN {0}'.format(self.propts))
        for v in self.getpropts():
            yield v