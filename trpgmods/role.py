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
        self.noend = True
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

    def focus_out_thing(self):
        return (self.getpropts(), self.name, 'thing', False)

    def focus_in_thing(self, thing):
        return {'curr_func': self.focus_out_propts, 'arg': (thing,), 'next_func': self.focus_in_propts}

    def focus_out_propts(self, thing):
        return (thing.getpropts(), thing.name, 'propts', True)

    def focus_in_propts(self, items):
        # インポート部分
        from game import Game

        return {'curr_func': self.act, 'arg': (items,), 'next_func': Game.argdic_first}

    def on(self, items):
        """ 比較リストに追加（Equip） """
        # インポート部分
        from game import Game

        # 検証
        for i in items:
            for j in self.thing.getpropts():
                # 比較リストに追加
                if i == j:
                    self.thing.f_compare.append(j)
                    self.thing.propts.remove(j.name)
        print('on 完了')
        return Game.dummy()

    def off(self, items):
        """ 比較リストから削除（UnEquip） """
        # インポート部分
        from game import Game

        # 検証
        for i in items:
            for j in self.thing.f_compare:
                # アイテムリストに追加
                if i == j:
                    self.thing.propts.append(j.name)
                    self.thing.f_compare.remove(j)
        print('off 完了')
        return Game.dummy()

    def choice(self, items):
        """ 交換リストを更新 """
        # インポート部分
        from game import Game

        # 元のアイテムリストに戻す
        self.thing.propts.extend([i.name for i in self.thing.f_xchange])
        self.thing.f_xchange.clear()

        # 検証
        for i in items:
            for j in self.thing.getpropts():
                # 交換リストに代入
                if i == j:
                    self.thing.f_xchange.append(j)
                    self.thing.propts.remove(j.name)
        print('change 完了')
        return Game.dummy()
    
    def way_node(self, node):
        # インポート部分
        from game import Game
        
        self.node = node

        return Game.dummy()

    def way_in(self, *dummy):
        # インポート部分
        from game import Game

        self.index = self.routes.index(self.node.name)
        if self.noend:
            self.noend = self.node.noend
            return {'curr_func': self.node.event().focus_out_first, 'arg': (self,), 'next_func': self.node.event().focus_in_first}
        else:
            self.noend = True
            return {'curr_func': Game.dummy, 'arg': (), 'next_func': Game.argdic_first}

    def way_out(self, *dummy):
        # インポート部分
        from game import Game
        
        self.node.occur()
        self.node = self.node.next
        self.routes[self.index] = self.node.name
        self.ordered = dict([('sbj', dict()), ('obj', dict())])

        return Game.dummy()
    
    def order(self, param):
        """ Generator """
        self.propts = [i.name for i in sorted(self.getpropts(), key=lambda x: x.point(param))]
        self.propts.reverse()
        print('ORDER IN {0}'.format(self.propts))
        for v in self.getpropts():
            yield v

    def action_out(self):
        """ Response Out """
        actlis = [self.on, self.off, self.choice]
        actlis.extend(self.getroutes())
        return (actlis, self.name, 'action', False)

    def action_in(self, act):
        """ Request In """
        # インポート部分
        from basemods import Holder

        if act is None:
            act = self.getroutes()[0]
        self.act = act

        if type(act) is Holder.classt('Route'):
            return {'curr_func': self.way_node, 'arg': (act,), 'next_func': self.way_in}
        else:
            return {'curr_func': self.focus_out_thing, 'arg': (), 'next_func': self.focus_in_thing}