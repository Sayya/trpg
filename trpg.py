import math
import random

class Dice:
    def __init__(self, times, maxim):
        self.times = times
        self.maxim = maxim

    def dice(self):
        return sum(random.randint(1, self.maxim) for i in range(self.times))

    def center(self):
        return self.times * self.maxim / 2

class Param():
    def __init__(self, name, dic, dice):
        self.name = name
        self.weight = dic
        self.dice_cls = dice

    def dice(self):
        return self.dice_cls.dice()

    def center(self):
        return self.dice_cls.center()

class Thing:
    def __init__(self, name, dic):
        self.name = name
        self.params = dic

    def point(self, paramd):
        p = self.params
        s = self.params[paramd.name]
        w = paramd.weight

        n = sum(p[i] * w[i] for i in w.keys()) + s

        return n * paramd.dice()

    def borderline(self, paramd):
        p = self.params
        s = self.params[paramd.name]
        w = paramd.weight

        n = sum(p[i] * w[i] for i in w.keys()) + s

        return n * paramd.center()

class Game:
    def __init__(self, paramd):
        self.paramd = paramd
        self.obj = 0
        self.subj = 0

    def compare(self):
        return self.subj - self.obj

    def subject_point(self, subj):
        self.subj = subj.point(self.paramd)
        return self.subj

    def object_borderline(self, obj):
        self.obj = obj.borderline(self.paramd)
        return self.obj