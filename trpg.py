import math
import random

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

class Param:
    """ Thingの属性（パラメータ）になる """
    master = dict()

    def __init__(self, name, dic, dice):
        self.name = name

        # {"name": int}
        self.weight = dic

        Param.master[self.name] = self

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

class Thing:
    """ 対象となるもの、オブジェクト """
    master = dict()
    pid = 0

    def __init__(self, name, dic, lis):
        self.name = name

        # {"name": Param()}
        self.params = dic

        # [Thing()]
        self.propts = lis
        self.f_compare = list()
        self.f_xchange = list()

        self.pid = Thing.pid
        Thing.pid += 1

        Thing.master[self.name] = self

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

class Process:
    """ Thingの属性（パラメータ）になる② """
    master = dict()

    def __init__(self, name, param0, param1, param2):
        self.name = name
        self.target = param0

        self.sbj_param = param1
        self.obj_param = param2

        Process.master[self.name] = self

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

        if n <= 0:
            r = 0
        else:
            r = obj.fluctuate(self.target, -1 * n)
            print(obj.name, 'の', self.target.name, 'は', int(r * 100), 'になった')

        if r <= 0:
            print(obj.name, 'はもう', self.target.name, 'できない')
            return 0
        else:
            return 1

class Role:
    """ 権限の単位、TRPGにおけるPL、PCのPLにあたる """
    master = dict()

    def __init__(self, name, dic):
        self.name = name

        # {"name": Thing()}
        self.propts = dic
        
        Role.master[self.name] = self

class Event:
    """ イベント """
    master = dict()

    def __init__(self, name, role, dhings, deed, n, text):
        self.name = name
        self.role = role

        self.sbj = Thing('', dict(), list()) if dhings[0] == None else dhings[0]
        self.obj = Thing('', dict(), list()) if dhings[1] == None else dhings[1]
        
        # Process のメソッド
        self.do = lambda: deed(self.sbj, self.obj)
        self.n = n

        self.text = text

        Event.master[self.name] = self
        
    def focus(self):
        if self.text != '':
            print(self.text)

        if self.n == 1 or self.n == 3:
            self.sbj = self.dialg(self.role.name, self.role)
        
        if self.n == 2 or self.n == 3:
            self.obj = self.dialg(self.role.name, self.role)

    def dialg(self, prompt, role):
        print(prompt, '> ', end='')
        nam = input()
        nli = nam.split('.')
        if len(nli) == 1 and nli[0] != '':
            return role.propts[nli[0]]
        elif len(nli) == 2:
            return role.propts[nli[0]].propts[nli[1]]

class Route:
    """
    ルーティング処理
    1. テキストによる状況説明
    2. 以下のうち一つか複数
    ・Processの繰り返し、中断（compare, fluctuate, next）
    ・Thingsの比較（compare）
    ・Thingの交換（xchange）
    ・Thingのパラム変更（vchange）

    ・生成（Product）
    ・Eventの挿入
    """
    master = dict()

    def __init__(self, name, dic, noend, event):
        self.name = name

        # {"name": (min, max)}
        self.route = dic

        # Boolean
        self.noend = noend
        
        self.event = event
        
        self.next = self
        Route.master[self.name] = self
        
    def occur(self):
        self.event.focus()
        n = self.event.do()
        self.next = self.routing(n)
    
    def routing(self, n):
        """ ルーティングの設計 """
        for i in sorted(self.route.keys()):
            if self.route[i][0] <= n < self.route[i][1] or self.route[i][0] == n:
                return Route.master[i]
        else:
            return self

class Game:
    def __init__(self, route):
        self.route = route
    
    def start(self):
        endflg = True
        while endflg:
            endflg = self.route.noend
            self.route.occur()
            self.route = self.route.next
