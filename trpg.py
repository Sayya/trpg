import math
import random

class Dice:
    """ 2d6形式を表現できる乱数クラス """
    def __init__(self, times, maxim, offset=0):
        self.times = times
        self.maxim = maxim
        self.offst = offset

        # 戻値：数値
        self.dice = lambda: sum(random.randint(1, self.maxim) for i in range(self.times)) + self.offst
        self.ceil = lambda: self.times * self.maxim + self.offst
        self.wall = lambda: self.times * (self.maxim + 1) / 2 + self.offst
        self.flor = lambda: self.times * self.maxim + self.offst

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

    def __init__(self, name, dic1, dic2):
        self.name = name
        self.params = dic1
        self.propts = dic2
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

    def change(self, param, n):
        self.p_ratio[param.name] = (self.bar(param) + n) / self.siz(param)

class Roll:
    """ 権限の単位、TRPGにおけるPL、PCのPLにあたる """
    def __init__(self, name, dic):
        self.name = name
        self.propts = dic


class Multi:
    """ Thingの属性（パラメータ）になる② """
    master = dict()

    def __init__(self, name, param0, param1, param2):
        self.name = name
        self.target = param0

        self.sbj_param = param1
        self.obj_param = param2

        Multi.master[self.name] = self

    # ２つのThingが競う
    def compare(self, sbj, obj):
        sbj_things_sum = sum(sbj.propts[i].point(self.target) for i in sbj.propts.keys() if self.target.name in sbj.propts[i].params) + 1
        obj_things_sum = sum(obj.propts[i].point(self.target) for i in obj.propts.keys() if self.target.name in sbj.propts[i].params) + 1
        
        offence = sbj.point(self.target) * sbj_things_sum * self.target.dice() + sbj.point(self.sbj_param)
        defence = obj.point(self.target) * obj_things_sum * self.target.dice() + obj.point(self.obj_param)
        
        return offence - defence

class Progress:
    """
    1. 比較し結果を得る
    2. 結果をもとにパラメータを変動させる
    3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
    """
    
    def __init__(self, multi, sbj, obj):
        self.multi = multi
        self.sbj = sbj
        self.obj = obj

    def compare(self):
        return self.multi.compare(self.sbj, self.obj)

    def change(self, n):
        """ n: self.compare() の戻り値 """
        self.obj.change(self.multi.target, n)
        return self.obj.p_ratio[self.multi.target.name]

    def next(self, r):
        """ r: self.change() の戻り値 """
        if r <= 0:
            return False
        else:
            return True

class Gate:
    """
    Thingのパラメータへ干渉するための関門 
    1. コスト管理
    """
    def __init__(self):
        pass
    
    def add(self, thing, param, n):
        thing.params[param.name] += n

class Select:
    """ 選択の設計 """
    def __init__(self):
        pass

class Place:
    """ 場所の設計 """
    def __init__(self):
        pass

class Event:
    """ イベントの設計 """
    def __init__(self):
        pass

class Game:
    def __init__(self):
        pass
