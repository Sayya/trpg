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
        self.params = dic

        self.propts = lis
        self.f_compare = list()
        self.f_xchange = list()

        self.pid = Thing.pid
        Thing.master[Thing.pid] = self
        Thing.pid += 1

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

    def change(self, param, n):
        self.params[param.name] += n

class Process:
    """ Thingの属性（パラメータ）になる② """
    master = dict()

    def __init__(self, name, param0, param1, param2):
        self.name = name
        self.target = param0

        self.sbj_param = param1
        self.obj_param = param2

        Process.master[self.name] = self
    
    def vchange(self, sbj, obj):
        obj.change(self.target, sbj.point(self.target))

    # あるパラメータについて２つのThingにおける交換
    def xchange(self, sbj, obj):
        sbj_propts_target = [i for i in sbj.f_xchange if self.target.name in sbj.f_xchange[i].params]
        sbj_propts_nonget = [i for i in sbj.f_xchange if self.target.name not in sbj.f_xchange[i].params]
        obj_propts_target = [i for i in obj.f_xchange if self.target.name in obj.f_xchange[i].params]
        obj_propts_nonget = [i for i in obj.f_xchange if self.target.name not in obj.f_xchange[i].params]

        sbj.f_xchange = sbj_propts_nonget.extend(obj_propts_target)
        obj.f_xchange = obj_propts_nonget.extend(sbj_propts_target)

    # あるパラメータについて２つのThingにおける差
    def compare(self, sbj, obj):
        sbj_propts_sum = sum(sbj.f_compare[i].point(self.target) for i in sbj.f_compare.keys() if self.target.name in sbj.f_compare[i].params) + 1
        obj_propts_sum = sum(obj.f_compare[i].point(self.target) for i in obj.f_compare.keys() if self.target.name in sbj.f_compare[i].params) + 1
        
        offence = sbj.point(self.target) * sbj_propts_sum * self.target.dice() + sbj.point(self.sbj_param)
        defence = obj.point(self.target) * obj_propts_sum * self.target.dice() + obj.point(self.obj_param)
        
        return offence - defence

    def fluctuate(self, obj, n):
        """ n: self.compare() の戻り値 """
        obj.fluctuate(self.target, n)
        return obj.p_ratio[self.target.name]

    def next(self, r):
        """
        r: self.fluctuate() の戻り値
        1. 比較し結果を得る
        2. 結果をもとにパラメータを変動させる
        3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
        """
        if r <= 0:
            return False
        else:
            return True

class Role:
    """ 権限の単位、TRPGにおけるPL、PCのPLにあたる """
    def __init__(self, name, dic):
        self.name = name
        self.propts = dic

class Select:

    def __init__(self, dic):
        self.roles = dic

class Product:
    master = dict()

    """ イベントの設計 """
    def __init__(self, name, prog, lis):
        self.name = name
        self.event = lis
        Product.master[self.name] = self

class Event:
    """
    イベント処理
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

    """ ルーティングの設計 """
    def __init__(self, name, dic, deed, noend):
        self.name = name
        self.route = dic
        self.deed = deed
        self.noend = noend
        Event.master[self.name] = self
    
    def next(self):
        n = self.deed()
        for i in sorted(self.route.keys()):
            if n < self.route[i]:
                return Event.master[i]
        else:
            return Event.master[sorted(self.route.keys())[0]]
class Game:
    def __init__(self, event):
        self.event = event
    
    def start(self):
        while self.event.noend:
            self.event = self.event.next()
