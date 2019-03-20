import math
import random

class TrpgError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Master:
    master = dict()
    pid = 0
    def __init__(self, name, *args):
        self.name = name
        self.cls = self.__class__

        if self.cls.pid == 0:
            self.cls.pid += 1
            self.cls('', *args)
        else:
            self.cls.pid += 1

        if self.name not in self.cls.master.keys():
            self.cls.master[self.name] = self
        else:
            raise TrpgError('すでに名前-{0}-のオブジェクト-{1}-は存在します'.format(self.name, self.cls.__name__))

class Dice:
    """ 2d6形式を表現できる乱数クラス """
    def __init__(self, times, maxim, offset=0):
        self.times = times
        self.maxim = maxim
        self.offset = offset

        # 戻値：数値
        self.dice = lambda: sum(random.randint(1, self.maxim) for i in range(self.times)) + self.offset

        self.ceil = lambda: self.times * self.maxim + self.offset
        self.wall = lambda: self.times * (self.maxim + 1) / 2 + self.offset
        self.flor = lambda: self.times * self.maxim + self.offset

class Param(Master):
    """ Thingの属性（パラメータ）になる """
    master = dict()
    pid = 0
    def __init__(self, name, dic, dice):
        super().__init__(name, dict(), Dice(0, 0))

        # {"name": int}
        self.weight = dic

        # pointA: 重み(0 <= n <= 1)とパラメータ(params[i])の数値を掛けたものの和
        self.pointA = lambda params: sum(Param.master[i].point(params) * self.weight[i] for i in self.weight.keys() if i != self.name)
        # pointB: 当クラスのパラメータ(params[self.name])の数値に重みを掛けた数値
        self.pointB = lambda params: params[self.name] * self.weight[self.name] if self.name in params else 0

        # pointAとpointBの和、pointAで遡って子Paramの重み計算が動的にできる
        # 引数：Thingの固有パラメータリスト
        # 戻値：数値
        self.point = lambda params: self.pointA(params) + self.pointB(params)

        # 戻値：数値
        self.dice = dice.dice
        self.ceil = dice.ceil
        self.wall = dice.wall

class Thing(Master):
    """ 対象となるもの、オブジェクト """
    master = dict()
    pid = 0
    def __init__(self, name, dic, lis):
        super().__init__(name, dict(), list())

        # {"name": Param()}
        self.params = dic

        # [Thing()]
        self.propts = lis
        self.f_compare = list()
        self.f_xchange = list()

        # パーセンテージ（HPなど）
        self.p_ratio = dict()
        for i in self.params.keys():
            self.p_ratio[i] = 1

        # 引数：対象のパラメータ
        self.point = lambda param: param.point(self.params)
        self.siz = lambda param: self.point(param) * param.ceil()
        self.bar = lambda param: self.siz(param) * self.p_ratio[param.name]

    def fluctuate(self, param, n):
        self.p_ratio[param.name] = (self.bar(param) + n) / self.siz(param)
        return self.p_ratio[param.name]

    def change(self, param, n):
        self.params[param.name] += n
        return self.params[param.name]

class Process(Master):
    """ Thingの属性（パラメータ）になる② """
    master = dict()
    pid = 0
    def __init__(self, name, param0, param1, param2):
        if len(Param.master) > 0:
            super().__init__(name, Param.master[''], Param.master[''], Param.master[''])
        else:
            raise TrpgError('オブジェクト-{0}-を先に生成してください'.format(Param.__name__))

        self.target = param0

        self.sbj_param = param1
        self.obj_param = param2

        # Event.deed の設定用
        self.point = lambda sbj, obj: obj.point(self.target)
        self.siz = lambda sbj, obj: obj.siz(self.target)
        self.bar = lambda sbj, obj: obj.bar(self.target)

        self.dice = lambda sbj, obj: self.target.dice()
        self.ceil = lambda sbj, obj: self.target.ceil()
        self.wall = lambda sbj, obj: self.target.wall()
        self.flor = lambda sbj, obj: self.target.flor()
    
    def vchange(self, sbj, obj):
        return obj.change(self.target, sbj.point(self.target))

    # あるパラメータについて２つのThingにおける交換
    def xchange(self, sbj, obj):
        sbj_propts_target = [i for i in sbj.f_xchange if self.target.name in sbj.f_xchange[i].params]
        sbj_propts_nonget = [i for i in sbj.f_xchange if self.target.name not in sbj.f_xchange[i].params]
        obj_propts_target = [i for i in obj.f_xchange if self.target.name in obj.f_xchange[i].params]
        obj_propts_nonget = [i for i in obj.f_xchange if self.target.name not in obj.f_xchange[i].params]

        sbj.f_xchange = sbj_propts_nonget.extend(obj_propts_target)
        obj.f_xchange = obj_propts_nonget.extend(sbj_propts_target)

        return 1

    # あるパラメータについて２つのThingにおける差
    def compare(self, sbj, obj):
        sbj_propts_sum = sum(i.point(self.target) for i in sbj.f_compare if self.target.name in i.params) + 1
        obj_propts_sum = sum(i.point(self.target) for i in obj.f_compare if self.target.name in i.params) + 1
        
        offence = sbj.point(self.target) * sbj_propts_sum * self.target.dice() + sbj.point(self.sbj_param)
        defence = obj.point(self.target) * obj_propts_sum * self.target.dice() + obj.point(self.obj_param)
        
        print(sbj.name, 'の', self.target.name, 'は', int(offence - defence))
        return offence - defence

    def fluctuate(self, sbj, obj):
        """
        1. 比較し結果を得る
        2. 結果をもとにパラメータを変動させる
        3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
        """
        n = self.compare(sbj, obj)

        if n < 0:
            n = 0
        
        r = obj.fluctuate(self.target, -1 * n)
        print(obj.name, 'の', self.target.name, 'は', int(r * 100), 'になった')

        if r <= 0:
            print(obj.name, 'はもう', self.target.name, 'できない')
            return 0
        else:
            return 1

class Role(Master):
    """ 権限の単位、TRPGにおけるPL、PCのPLにあたる """
    master = dict()
    pid = 0
    def __init__(self, name, lis1, lis2):
        super().__init__(name, list(), list())

        # [Thing()] => {"name": Thing()}
        self.propts = {v.name: v for v in lis1}

        # [Route()] => {"name": Route()}
        self.routes = {v.name: v for v in lis2}

        self.thing = Thing.master['']
        self.items = list()

    def action(self):
        
        def focus():
            print('IN {0}'.format(list(self.propts.keys())))
            print('[{0}]:{1}'.format(self.name, 'thing'), '> ', end='')
            nam = input()
            if nam in self.propts:
                self.thing = self.propts[nam]
            else:
                raise TrpgError('Role-{0}-はThing-{1}-を所有していません'.format(self.name, nam))
            
            if len(self.thing.propts) != 0:
                print('IN {0}'.format(list(self.thing.propts.keys())))
                print('[{0}]:{1}'.format(self.name, 'propts'), '> ', end='')
                nam = input()
                self.items = nam.split(',')
            else:
                raise TrpgError('Thing-{0}-は他のThingを所有していません'.format(self.thing.name))

        def on ():
            # 検証
            for i in self.items:
                for j in self.thing.propts:
                    # 比較リストに追加
                    if i == j.name:
                        self.thing.f_compare.append(j)
                        self.thing.propts.remove(j)

        def off():
            # 検証
            for i in self.items:
                for j in self.thing.f_compare:
                    # アイテムリストに追加
                    if i == j.name:
                        self.thing.propts.append(j)
                        self.thing.f_compare.remove(j)

        def choice():
            # 元のアイテムリストに戻す
            self.thing.propts.extend(self.thing.f_xchange[:])
            self.thing.f_xchange.clear()

            # 検証
            for i in self.items:
                for j in self.thing.propts:
                    # 交換リストに代入
                    if i == j.name:
                        self.thing.f_xchange.append(j)
                        self.thing.propts.remove(j)
        
        actlist = ['on', 'off', 'choice']
        actlist.extend(list(self.routes.keys()))
        print('IN {0}'.format(actlist))
        print('[{0}]:{1}'.format(self.name, 'action'), '> ', end='')
        nam = input()
        try:
            if nam == 'on':
                focus()
                on()
            elif nam == 'off':
                focus()
                off()
            elif nam == 'choice':
                focus()
                choice()
            elif nam in self.routes.keys():
                Event.sbj_role = self
                Event.obj_role = self
                
                endflg = True
                while endflg:
                    endflg = self.routes[nam].noend
                    self.routes[nam].occur()
                    self.routes[nam] = self.routes[nam].next

        except TrpgError as e:
            print('MESSAGE:', e.value)
            
    def order_by(self, param):
        self.propts = dict(sorted(self.propts, key=lambda x: x.point(param)))
        
    def order_next(self):
        for v in self.propts.values():
            yield v

    def dialg_thing(self, desc):
        print('IN {0}'.format(list(self.propts.keys())))
        print('[{0}]:{1}'.format(self.name, desc), '> ', end='')
        nam = input()
        nli = nam.split('.')

        rslt = Thing.master['']

        if 0 < len(nli) < 3 and nli[0] in self.propts:
            if len(nli) == 1:
                rslt = self.propts[nli[0]]
            elif len(nli) == 2 and nli[1] in self.propts[nli[0]]:
                rslt = self.propts[nli[0]].propts[nli[1]]
        
        return rslt

    @classmethod
    def dialog_role(self):
        print('IN {0}'.format(list(Role.master.keys())[1:]))
        print('[{0}]:{1}'.format('Game', 'role'), '> ', end='')

        nam = input()
        if nam != '' and nam in Role.master.keys():
            return Role.master[nam]
        else:
            raise TrpgError('Role-{0}-は存在しません'.format(nam))

class Event(Master):
    """ イベント """
    master = dict()
    pid = 0
    sbj_role = None
    obj_role = None

    def __init__(self, name, defthings, deed, rolething, text):
        """
        m について
        m = 0: 使用するRoleはEvent.role
        m = 1: 使用するRoleをdialgでEvent.roleに設定
        n について
        n = 1: self.sbjのみdialg指定
        n = 2: self.objのみdialg指定
        n = 3: self.sbj, self.objどちらもdialg指定
        n = 上記以外: デフォルトのdhingsを指定
        """
        super().__init__(name, (None, None), (lambda: 0, Param.master['']), (0, 0, 0, 0), '')

        if len(Thing.master) > 0:
            if len(defthings) == 2:
                self.sbj = defthings[0] if isinstance(defthings[0], Thing) else Thing.master['']
                self.obj = defthings[1] if isinstance(defthings[1], Thing) else Thing.master['']
            else:
                raise TrpgError('引数-{0}-のリストサイズが２ではありません'.format('defthings'))
        else:
            raise TrpgError('オブジェクト-{0}-を先に生成してください'.format(Thing.__name__))
        
        # Process のメソッド
        self.do = lambda: deed[0](self.sbj, self.obj)
        self.target = deed[1]
        self.role1_f = rolething[0]
        self.sbj_f = rolething[1]
        self.role2_f = rolething[2]
        self.obj_f = rolething[3]
        
        self.text = text
        
    def focus(self):
        if self.text != '':
            print(self.text)

        try:
            if self.role1_f == 1 or Event.sbj_role == None:
                Event.sbj_role = Role.dialog_role()

            if self.sbj_f == 1:
                self.sbj = Event.sbj_role.dialg_thing('sbj')
            elif self.sbj_f == 2:
                Event.sbj_role.order_by(self.target)
                self.sbj = Event.sbj_role.order_next()

            if self.role2_f == 1 or Event.obj_role == None:
                Event.obj_role = Role.dialog_role()
            
            if self.obj_f == 1:
                self.obj = Event.obj_role.dialg_thing('obj')
            elif self.obj_f == 2:
                Event.obj_role.order_by(self.target)
                self.obj = Event.obj_role.order_next()
                
        except TrpgError as e:
            print('MESSAGE:', e.value)

class Route(Master):
    """
    ルーティング処理
    1. テキストによる状況説明
    2. 以下のうち一つか複数
    ・Processの繰り返し、中断（compare, fluctuate, next）
    ・Thingsの比較（compare）
    ・Thingの交換（xchange）
    ・Thingのパラム変更（vchange）

    ・生成（Product）
    """
    master = dict()
    pid = 0
    def __init__(self, name, dic, noend, event):
        if len(Event.master) > 0:
            super().__init__(name, dict(), True, Event.master[''])
        else:
            raise TrpgError('オブジェクト-{0}-を先に生成してください'.format(Event.__name__))

        # {"name": (min, max)}
        self.route = dic

        # Boolean
        self.noend = noend
        
        self.event = event
        
        self.next = self
        
    def occur(self):
    
        def routing(n):
            """ ルーティングの設計 """
            for i in sorted(self.route.keys()):
                if self.route[i][0] <= n < self.route[i][1] or self.route[i][0] == n:
                    return Route.master[i]
            else:
                return self

        self.event.focus()
        n = self.event.do()
        self.next = routing(n)

class Game:
    def __init__(self, lis):

        # [Role()]
        self.roles = lis
    
    def start(self):
        endflg = True
        while endflg:
            for i in self.roles:
                i.action()