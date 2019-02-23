import math
import random

def dice(x, y):
    n = sum(random.randint(1, y) for i in range(x))
    return n

class Prime:
    def __init__(self, dic):
        self.params = dict()
        for k in dic.keys():
            self.params[k] = dic[k]
        
    def geti(self, x):
        return self.params[x]

class Skill:
    def __init__(self, name, dic):
        self.name = name
        self.weight = dict()
        for k in dic.keys():
            self.weight[k] = dic[k]

    def getw(self, name):
        return self.weight[name]

class Charactor:
    def __init__(self, name, dic):
        self.name = name
        self.skills = Prime(dic)
        self.params = Prime({
            "POW": dice(2, 6),
            "SEN": dice(2, 6),
            "INT": dice(2, 6),
        })

    def getSP(self, skill):
        p = self.params
        s = self.skills.geti(skill.name)
        r = skill.weight.keys()

        n = sum(p.geti(i) * skill.getw(i) for i in r) + s

        return n

class Test:
    def __init__(self):
        self.s1 = Skill("Swimming", {"POW": 0.1})
        self.c1 = Charactor("C01", {"Swimming": dice(2, 6)})

    def test01(self, times):

        result = []
        for i in range(times):
            result.append(self.c1.getSP(self.s1) * dice(2, 6))
            print(self.c1.name , '-', self.s1.name, ':', int(result[i]))
        
        print("Avarage :", sum(result) / len(result))

