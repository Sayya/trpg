import math
import random

class Dice:
    """ 2d6形式を表現できる乱数クラス """
    def __init__(self, times, maxim):
        self.times = times
        self.maxim = maxim
        self.dice = lambda: sum(random.randint(1, self.maxim) for i in range(self.times))
        self.wall = lambda: self.times * self.maxim / 2

class Param():
    """ Thingの属性（パラメータ）になる """
    master = dict()

    def __init__(self, name, dic, dice):
        self.name = name
        self.weight = dic
        Param.master[self.name] = self

        # pointA: 重み(0 <= n <= 1)とパラメータ(params[i])の数値を掛けたものの和
        self.pointA = lambda params: sum(Param.master[i].point(params) * self.weight[i] for i in self.weight.keys())
        # pointB: 当クラスのパラメータ(params[self.name])の数値に残りの重みパーセンテージ(1 - sum(n))をかけた数値
        self.pointB = lambda params: params[self.name] * (1 - sum(self.weight[i] for i in self.weight.keys()))
        # pointAとpointBの和、pointAで遡って各子Paramの重み計算が動的にできる
        self.point = lambda params: self.pointA(params) + self.pointB(params)

        self.dice = dice.dice
        self.wall = dice.wall

class Thing:
    """ 対象となるもの、オブジェクト """
    def __init__(self, name, dic):
        self.name = name
        self.params = dic

        # パーセンテージ（HPなど）
        self.params_tmp = dict()
        for i in self.params:
            self.params_tmp[i] = 1

        self.point = lambda param: param.point(self.params)

        self.dice = lambda param: self.point(param) * param.dice()
        self.wall = lambda param: self.point(param) * param.wall()

class Progress:
    """
    1. 比較し結果を得る
    2. 結果をもとにパラメータを変動させる
    """
    def __init__(self):
        pass

class Game:
    """ 引数にParamを一つ渡し、それについて２つのThingが競う """
    def __init__(self, param):
        self.param = param
        
        self.point = lambda subj: subj.dice(self.param)
        self.wall = lambda obj: obj.wall(self.param)

        self.compare = lambda subj, obj: subj.dice(self.param) - obj.center(self.param)