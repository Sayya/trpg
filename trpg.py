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
            self.pid = self.cls.pid
            self.cls.pid += 1

        if self.name in self.cls.master.keys():
            raise TrpgError('すでに名前-{0}-のオブジェクト-{1}-は存在します'.format(self.name, self.cls.__name__))
        
        self.cls.master[self.name] = self

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
    def __init__(self, name, dic=dict(), dice=Dice(0, 0)):
        super().__init__(name)

        # {Param().name: int}
        self.weight = dic

        # pointA: 重み(0 <= n <= 1)とパラメータ(Param.master[i])の数値を掛けたものの和
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
        self.flor = dice.flor

class Thing(Master):
    """ 対象となるもの、オブジェクト """
    master = dict()
    pid = 0
    def __init__(self, name, dic=dict(), lis=list()):
        super().__init__(name)

        # {Param().name: Param()}
        self.params = dic

        for i in lis:
            if i not in Thing.master.keys():
                raise TrpgError('{0}オブジェクト-{1}-を先に生成してください'.format(Param.__name__, i))

        # [Thing()]
        self.propts = [Thing.master[i] for i in lis]
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
    def __init__(self, name, param0='', deed='point', param1='', param2=''):
        """
        deed option:
        - point, siz, bar
        - dice, ceil, wall, flor
        - vchange, xchange, compare, increase, decrease
        """
        if len(Param.master) == 0:
            raise TrpgError('オブジェクト-{0}-を先に生成してください'.format(Param.__name__))
        
        super().__init__(name)

        self.target = Param.master[param0]

        self.sbj_param = Param.master[param1]
        self.obj_param = Param.master[param2]

        # Event.deedの設定
        self.deed = getattr(self, deed)

        # Event.deed の拡張
    def point(self, sbj, obj, n):
        rtn= obj.point(self.target)
        print('{0}\'s {1} point: {2}'.format(obj.name, self.target.name, rtn))
        return rtn

    def siz(self, sbj, obj, n): return obj.siz(self.target)
    def bar(self, sbj, obj, n): return obj.bar(self.target)
    def dice(self, sbj, obj, n): return self.target.dice()
        
    def ceil(self, sbj, obj, n): return self.target.ceil()
    def wall(self, sbj, obj, n): return self.target.wall()
    def flor(self, sbj, obj, n): return self.target.flor()
    
    def vchange(self, sbj, obj, n):
        return obj.change(self.target, sbj.point(self.target))

    # あるパラメータについて２つのThingにおける交換
    def xchange(self, sbj, obj, n):
        sbj_propts_target = [i for i in sbj.f_xchange if self.target.name in sbj.f_xchange[i].params]
        sbj_propts_nonget = [i for i in sbj.f_xchange if self.target.name not in sbj.f_xchange[i].params]
        obj_propts_target = [i for i in obj.f_xchange if self.target.name in obj.f_xchange[i].params]
        obj_propts_nonget = [i for i in obj.f_xchange if self.target.name not in obj.f_xchange[i].params]

        sbj.f_xchange = sbj_propts_nonget.extend(obj_propts_target)
        obj.f_xchange = obj_propts_nonget.extend(sbj_propts_target)

        return 1

    # あるパラメータについて２つのThingにおける差
    def compare(self, sbj, obj, n):
        sbj_propts_sum = sum(i.point(self.target) for i in sbj.f_compare if self.target.name in i.params) + 1
        obj_propts_sum = sum(i.point(self.target) for i in obj.f_compare if self.target.name in i.params) + 1
        
        offence = sbj.point(self.target) * sbj_propts_sum * self.target.dice() + sbj.point(self.sbj_param)
        defence = obj.point(self.target) * obj_propts_sum * self.target.dice() + obj.point(self.obj_param)
        
        print(sbj.name, 'の', self.target.name, 'は', int(offence - defence))
        return offence - defence

    def increase(self, sbj, obj, n):
        """
        1. 比較し結果を得る
        2. 結果をもとにパラメータを変動させる
        3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
        """
        if n < 0:
            n = 0
        
        r = obj.fluctuate(self.target, 1 * n)
        print(obj.name, 'の', self.target.name, 'は', int(r * 100), 'になった')

        if r >= 1:
            return 1
        else:
            return 0

    def decrease(self, sbj, obj, n):
        """
        1. 比較し結果を得る
        2. 結果をもとにパラメータを変動させる
        3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
        """
        if n < 0:
            n = 0
        
        r = obj.fluctuate(self.target, -1 * n)
        print(obj.name, 'の', self.target.name, 'は', int(r * 100), 'になった')

        if r <= 0:
            print(obj.name, 'はもう', self.target.name, 'できない')
            return 0
        else:
            return 1

class Event(Master):
    """ イベント """
    master = dict()
    pid = 0
    role = None
    sbj = None
    obj = None

    def __init__(self, name, procs='', rolething=(0, 1, 0), defthings=('',''), text=''):
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
        if len(Process.master) == 0:
            raise TrpgError('オブジェクト-{0}-を先に生成してください'.format(Process.__name__))

        if len(Thing.master) == 0:
            raise TrpgError('オブジェクト-{0}-を先に生成してください'.format(Thing.__name__))
        
        super().__init__(name)
        
        if len(defthings) != 2:
            raise TrpgError('引数-{0}-のリストサイズが２ではありません'.format('defthings'))

        if defthings[0] not in Thing.master.keys():
            raise TrpgError('Thing-{0}-は存在しません'.format(defthings[0]))

        self.sbj = Thing.master[defthings[0]]

        if defthings[1] not in Thing.master.keys():
            raise TrpgError('Thing-{0}-は存在しません'.format(defthings[1]))
        
        self.obj = Thing.master[defthings[1]]

        # Process のメソッド
        self.do = lambda n: Process.master[procs].deed(self.sbj, self.obj, n)
        self.target = Process.master[procs].target
        self.role_f = rolething[0]
        self.sbj_f = rolething[1]
        self.obj_f = rolething[2]
        
        self.text = text
        
    def focus(self):
        if self.text != '':
            print(self.text)

        try:
            # 主体の設定
            if self.role_f == 1 or self.role_f == 3 or Event.role == None:
                Event.role = Role.dialog_role()

            if self.sbj_f == 1:
                self.sbj = Event.role.dialg_thing('sbj')
            elif self.sbj_f == 2:
                Event.role.order_by(self.target)
                self.sbj = Event.role.order_next()

            # 客体の設定
            if self.role_f == 2 or self.role_f == 3 or Event.role == None:
                Event.role = Role.dialog_role()
            
            if self.obj_f == 1:
                self.obj = Event.role.dialg_thing('obj')
            elif self.obj_f == 2:
                Event.role.order_by(self.target)
                self.obj = Event.role.order_next()

            # クリーニング
            if self.sbj.name == '' and Event.sbj != None:
                self.sbj = Event.sbj
            else:
                Event.sbj = self.sbj
            
            if self.obj.name == '' and Event.obj != None:
                self.obj = Event.obj
            else:
                Event.obj = self.obj
                
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
    def __init__(self, name, event='', dic=dict(), prev=0, noend=True):
        if len(Event.master) == 0:
            raise TrpgError('オブジェクト-{0}-を先に生成してください'.format(Event.__name__))
        
        super().__init__(name)

        # {Route().name: (min, max)}
        self.route = dic

        # Boolean
        self.noend = noend
        
        self.event = Event.master[event]
        
        self.next = self

        self.prev = prev
        
    def occur(self):
    
        def routing(n):
            """ ルーティングの設計 """
            for i in self.route.keys():
                if self.route[i][0] == 'next' \
                or self.route[i][0] <= n < self.route[i][1] \
                or self.route[i][0] == n:
                    Route.master[i].prev = n
                    return Route.master[i]
            else:
                return self

        self.event.focus()
        self.prev = self.event.do(self.prev)
        self.next = routing(self.prev)

class Role(Master):
    """ 権限の単位、TRPGにおけるPL、PCのPLにあたる """
    master = dict()
    pid = 0
    def __init__(self, name, lis1=list(), lis2=list()):
        super().__init__(name)

        # [Thing().name] => {"name": Thing()}
        self.propts = {v: Thing.master[v] for v in lis1}

        # [Route().name] => {"name": Route()}
        self.routes = {v: Route.master[v] for v in lis2}

        self.thing = Thing.master['']
        self.items = list()

    def action(self):
        
        def focus():
            print('IN {0}'.format(list(self.propts.keys())))
            print('[{0}]:{1}'.format(self.name, 'thing'), '> ', end='')
            nam = input()
            if nam not in self.propts:
                raise TrpgError('Role-{0}-はThing-{1}-を所有していません'.format(self.name, nam))
            
            self.thing = self.propts[nam]
            
            if len(self.thing.propts) == 0:
                raise TrpgError('Thing-{0}-は他のThingを所有していません'.format(self.thing.name))
            
            print('IN {0}'.format(list(self.thing.propts.keys())))
            print('[{0}]:{1}'.format(self.name, 'propts'), '> ', end='')
            nam = input()
            self.items = nam.split(',')

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
                Event.role = self
                Event.role = self
                
                endflg = True
                while endflg:
                    endflg = self.routes[nam].noend
                    self.routes[nam].occur()
                    self.routes[nam] = self.routes[nam].next
                    print(self.routes[nam].name, self.routes[nam].noend)

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

        rtn = Thing.master['']

        if 0 < len(nli) < 3 and nli[0] in self.propts:
            if len(nli) == 1:
                rtn = self.propts[nli[0]]
            elif len(nli) == 2 and nli[1] in self.propts[nli[0]]:
                rtn = self.propts[nli[0]].propts[nli[1]]
        
        return rtn

    @classmethod
    def dialog_role(self):
        print('IN {0}'.format(list(Role.master.keys())[1:]))
        print('[{0}]:{1}'.format('Game', 'role'), '> ', end='')

        nam = input()
        if nam == '' or nam not in Role.master.keys():
            raise TrpgError('Role-{0}-は存在しません'.format(nam))
        
        return Role.master[nam]

class Game:
    def __init__(self, lis):

        # [Role()]
        self.roles = [Role.master[v] for v in lis]
    
    def start(self):
        endflg = True
        while endflg:
            for i in self.roles:
                i.action()
    

