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
            raise TrpgError('すでに名前 -{0}- の {1} オブジェクトは存在します'.format(self.name, self.cls.__name__))
        
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

    def __init__(self, \
        name:'str,名前', \
        weight:'dict-Param.name:int-0,重み'=dict(), \
        dice:'tuple-int-2,ダイス'=(0, 0)):

        super().__init__(name)

        # {Param().name: int}
        self.weight = weight

        # pointA: 重み(0 <= n <= 1)とパラメータ(Param.master[i])の数値を掛けたものの和
        self.pointA = lambda params: sum(Param.master[i].point(params) * self.weight[i] for i in self.weight.keys() if i != self.name)
        # pointB: 当クラスのパラメータ(params[self.name])の数値に重みを掛けた数値
        self.pointB = lambda params: params[self.name] * self.weight[self.name] if self.name in params else 0

        # pointAとpointBの和、pointAで遡って子Paramの重み計算が動的にできる
        # 引数：Thingの固有パラメータリスト
        # 戻値：数値
        self.point = lambda params: self.pointA(params) + self.pointB(params)

        gendice = Dice(*dice)
        # 戻値：数値
        self.dice = gendice.dice
        self.ceil = gendice.ceil
        self.wall = gendice.wall
        self.flor = gendice.flor

class Thing(Master):
    """ 対象となるもの、オブジェクト """
    master = dict()
    pid = 0

    def __init__(self, \
        name:'str,名前', \
        params:'dict-Param.name:int-0,パラメータ'=dict(), \
        propts:'list-Thing-0,所有'=list()):
        
        super().__init__(name)

        # {Param().name: Param()}
        self.params = params

        for i in propts:
            if i not in Thing.master.keys():
                raise TrpgError('{0} オブジェクト -{1}- は存在しません'.format(Param.__name__, i))

        # [Thing()]
        self.propts = [Thing.master[i] for i in propts]
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
    """ Event の主処理 """
    master = dict()
    pid = 0

    def __init__(self, \
        name:'str,名前', \
        target:'Param.name,主パラ'='', \
        deed:'Process.deed,処理'='', \
        sbj_param:'Param.name,能パラ'='', \
        obj_param:'Param.name,受パラ'=''):
        
        """
        deed option:
        - point, siz, bar
        - dice, ceil, wall, flor
        - vchange, xchange, compare, increase, decrease
        """

        if len(Param.master) == 0:
            raise TrpgError('{0} オブジェクトを先に生成してください'.format(Param.__name__))
        
        super().__init__(name)

        self.target = Param.master[target]

        self.sbj_param = Param.master[sbj_param]
        self.obj_param = Param.master[obj_param]

        # Event.deedの設定
        try:
            self.deed = getattr(self, deed)
        except:
            self.deed = lambda sbj, obj, n: 0

    # Event.deed の拡張
    def point(self, sbj, obj, n):
        rtn = obj.point(self.target)

        print('{0} の -{1}- ポイントは {2}'.format(obj.name, self.target.name, rtn))
        return rtn

    def siz(self, sbj, obj, n):
        rtn = obj.siz(self.target)

        print('{0} の -{1}- 基準値は {2}'.format(obj.name, self.target.name, rtn))
        return rtn
    
    def bar(self, sbj, obj, n):
        rtn = obj.bar(self.target)

        print('{0} の -{1}- 変動値は {2}%'.format(obj.name, self.target.name, rtn))
        return rtn

    def dice(self, sbj, obj, n):
        rtn = self.target.dice()

        print('-{0}- は {1} になった'.format(self.target.name, rtn))
        return rtn
    
    def ceil(self, sbj, obj, n): return self.target.ceil()
    def wall(self, sbj, obj, n): return self.target.wall()
    def flor(self, sbj, obj, n): return self.target.flor()
    
    def reset(self, sbj, obj, n):
        r = obj.siz(self.target) - obj.bar(self.target)
        rtn = obj.fluctuate(self.target, 1 * r)

        print('{0} の -{1}- をリセットした'.format(obj.name, self.target.name))
        return rtn
    
    def vchange(self, sbj, obj, n):
        rtn = obj.change(self.target, sbj.point(self.target))

        print('{0} の -{1}- 値は {2}'.format(obj.name, self.target.name, rtn))
        return rtn

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

        rtn = offence - defence
        
        print('{0} の -{1}- は {2}'.format(sbj.name, self.target.name, int(rtn)))
        return rtn

    def increase(self, sbj, obj, n):
        """
        1. 比較し結果を得る
        2. 結果をもとにパラメータを変動させる
        3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
        """
        if n < 0:
            n = 0
        
        r = obj.fluctuate(self.target, 1 * n)
        
        print('{0} の -{1}- は {2}% になった'.format(obj.name, self.target.name, int(r * 100)))
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

        print('{0} の -{1}- は {2}% になった'.format(obj.name, self.target.name, int(r * 100)))
        if r <= 0:
            print('{0} はもう -{1}- できない'.format(obj.name, self.target.name))
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

    def __init__(self, \
        name:'str,名前', \
        procs:'Process.name,プロセス'='', \
        rolething:'tuple-int-3,(ロールフラグ.能フラグ.受フラグ)'=(0, 1, 0), \
        defthings:'tuple-Thing.name-2,(能者.受者)'=('',''), \
        text:'str,テキスト'=''):
        
        """
        """
        if len(Process.master) == 0:
            raise TrpgError('{0} オブジェクトを先に生成してください'.format(Process.__name__))

        if len(Thing.master) == 0:
            raise TrpgError('{0} オブジェクトを先に生成してください'.format(Thing.__name__))
        
        super().__init__(name)
        
        if len(defthings) != 2:
            raise TrpgError('引数 -{0}- のリストサイズが２ではありません'.format('defthings'))

        if defthings[0] not in Thing.master.keys():
            raise TrpgError('Thing -{0}- は存在しません'.format(defthings[0]))

        if defthings[1] not in Thing.master.keys():
            raise TrpgError('Thing -{0}- は存在しません'.format(defthings[1]))

        self.sbj = Thing.master[defthings[0]]
        
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
                Event.role = Arbit.dialog(Role)

            if self.sbj_f == 1:
                self.sbj = Arbit.dialg_propts(Event.role, 'sbj')
            elif self.sbj_f == 2:
                self.sbj = Arbit.order_next(Event.role, self.target.name)

            # 客体の設定
            if self.role_f == 2 or self.role_f == 3 or Event.role == None:
                Event.role = Arbit.dialog(Role)
            
            if self.obj_f == 1:
                self.obj = Arbit.dialg_propts(Event.role, 'obj')
            elif self.obj_f == 2:
                self.obj = Arbit.order_next(Event.role, self.target.name)

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

    def __init__(self, \
        name:'str,名前', \
        route:'dict-Route.name:tuple+int/next+2-0,ルート'=dict(), \
        event:'Event.name,イベント'='', \
        prev:'int,初期値'=0, \
        noend:'bool,継続'=True):
        
        if len(Event.master) == 0:
            raise TrpgError('{0} オブジェクトを先に生成してください'.format(Event.__name__))
        
        super().__init__(name)

        # {Route().name: (min, max)}
        self.route = route

        # Boolean
        self.noend = noend
        
        if event == '' and name in Event.master.keys():
            self.event = Event.master[name]
        elif event in Event.master.keys():
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

    def __init__(self, \
        name:'str,名前', \
        propts:'list-Thing.name-0,選択肢'=list(), \
        routes:'list-Route.name-0,選択ルート'=list()):
        
        super().__init__(name)

        # [Thing().name] => {"name": Thing()}
        self.propts = {v: Thing.master[v] for v in propts}

        # [Route().name] => {"name": Route()}
        self.routes = {v: Route.master[v] for v in routes}

        self.thing = Thing.master['']
        self.items = list()

    def action(self):
        
        def focus():
            print('IN {0}'.format(list(self.propts.keys())))
            print('[{0}]:{1}'.format(self.name, 'thing'), '> ', end='')
            nam = input()
            if nam not in self.propts:
                raise TrpgError('Role -{0}- は Thing -{1}- を所有していません'.format(self.name, nam))
            
            self.thing = self.propts[nam]
            
            if len(self.thing.propts) == 0:
                raise TrpgError('Thing -{0}- は他の Thing を所有していません'.format(self.thing.name))
            
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
                    # print(self.routes[nam].name, self.routes[nam].noend)

        except TrpgError as e:
            print('MESSAGE:', e.value)
        
    def order(self, param):
        self.propts = dict(sorted(self.propts, key=lambda x: x.point(param)))
        for v in self.propts.values():
            yield v

class Arbit(Master):
    """ Role を受け取り、AIがその中の Thing を返す """
    master = dict()
    pid = 0
    param = ''
    role = ''

    def __init__(self, \
        name:'str,名前', \
        role:'Role.name,ロール'=''):
        
        super().__init__(name)

    @classmethod
    def order_next(self, role, param):
        if Arbit.param != param:
            Arbit.param = param
            Arbit.order = Role.master[role].order(Param.master[param])
        
        try:
            rtn = next(Arbit.order)
        except StopIteration:
            return None
        else:
            return rtn

    @classmethod
    def dialog(self, elem):
        print('IN {0}'.format(list(elem.master.keys())[1:]))
        print('[{0}]:{1}'.format('Arbit', elem.__name__), '> ', end='')

        nam = input()
        if nam == '' or nam not in elem.master.keys():
            raise TrpgError('{0} オブジェクト -{1}- は存在しません'.format(elem.__name__, nam))
        
        return elem.master[nam]

    @classmethod
    def dialg_propts(self, role, desc):
        print('IN {0}'.format(list(role.propts.keys())))
        print('[{0}]:{1}'.format(role.name, desc), '> ', end='')
        nam = input()
        nli = nam.split('.')

        rtn = role.propts[list(role.propts.keys())[0]]

        if 0 < len(nli) < 3 and nli[0] in role.propts:
            if len(nli) == 1:
                rtn = role.propts[nli[0]]
            elif len(nli) == 2 and nli[1] in role.propts[nli[0]]:
                rtn = role.propts[nli[0]].propts[nli[1]]
        
        return rtn

class Game:
    def __init__(self, roles):

        # [Role()]
        self.roles = [Role.master[v] for v in roles]
    
    def start(self):
        endflg = True
        while endflg:
            for i in self.roles:
                i.action()
    

