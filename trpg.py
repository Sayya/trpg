import math
import random

class Dice:
    """ 2d6形式を表現できる乱数クラス """
    def __init__(self, times, maxim):
        self.times = times
        self.maxim = maxim

        # 戻値：数値
        self.dice = lambda: sum(random.randint(1, self.maxim) for i in range(self.times))
        self.ceil = lambda: self.times * self.maxim
        self.wall = lambda: self.ceil() / 2

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
        self.pointB = lambda params: params[self.name] * self.weight[self.name]

        # pointAとpointBの和、pointAで遡って子Paramの重み計算が動的にできる
        # 引数：Thingの固有パラメータリスト
        # 戻値：数値
        self.point = lambda params: self.pointA(params) + self.pointB(params)

        # 戻値：数値
        self.dice = dice.dice
        self.ceil = dice.ceil
        self.wall = dice.wall

class Multi:
    """ Thingの属性（パラメータ）になる② """
    master = dict()

    def __init__(self, name, param1, param2, param3):
        self.name = name
        self.main = param1
        self.subj_modif = param2
        self.obj_modif = param3
        Multi.master[self.name] = self

    # ２つのThingが競う
    def compare(self, subj, obj):
        offence = subj.dice(self.main) + subj.point(self.subj_modif)
        defence = obj.wall(self.main) + obj.point(self.obj_modif)
        return offence - defence

class Thing:
    """ 対象となるもの、オブジェクト """
    def __init__(self, name, dic):
        self.name = name
        self.params = dic

        # パーセンテージ（HPなど）
        self.p_ratio = dict()
        for i in self.params:
            self.p_ratio[i] = 1

        # 引数：対象のパラメータ
        self.point = lambda param: param.point(self.params)
        self.dice = lambda param: param.point(self.params) * param.dice()
        self.ceil = lambda param: param.point(self.params) * param.ceil()
        self.wall = lambda param: param.point(self.params) * param.wall()

        self.hp = lambda param: self.p_ratio[param.name] * self.ceil(param)

    def decreace(self, param, n):
        self.p_ratio[param.name] = (self.ceil(param) * self.p_ratio[param.name] - n) / self.ceil(param)

class Progress:
    """
    1. 比較し結果を得る
    2. 結果をもとにパラメータを変動させる
    3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
    """
    
    def __init__(self, multi):
        self.multi = multi

    def decreace(self, subj, obj):
        n = self.multi.compare(subj, obj)
        print(self.multi.name, 'damage:',  int(n))
        if n > 0:
            obj.decreace(self.multi.main, n)
        return obj.p_ratio[self.multi.main.name]

    def next(self, subj, obj):
        r = self.decreace(subj, obj)
        print(obj.name, 'HP:', int(obj.hp(self.multi.main)))
        print(obj.name, 'ratio:', int(r * 100), '%')
        if r <= 0:
            return False
        else:
            return True

class Event:
    """ イベントの設計 """
    def __init__(self):
        pass

class Game:
    def __init__(self):
        pass
