import math
import random

def dice(x, y):
    n = sum(random.randint(1, y) for i in range(x))
    return n

class Skill:
    def __init__(self, name, dic):
        self.name = name
        self.weight = dic

class Charactor:
    def __init__(self, name, dic):
        self.name = name
        self.skills = dic

    def getSP(self, skill):
        p = self.skills
        s = self.skills[skill.name]
        w = skill.weight

        n = sum(p[i] * w[i] for i in w.keys()) + s

        return n

class Test:
    def __init__(self):
        self.s = [
            Skill("POW1", dict()),
            Skill("POW2", dict()),
            Skill("POW3", dict()),
            Skill("SEN1", dict()),
            Skill("SEN2", dict()),
            Skill("SEN3", dict()),
            Skill("INT1", dict()),
            Skill("INT2", dict()),
            Skill("INT3", dict()),

            Skill("Swim", {"POW1": 0.1}),
            Skill("Hit", {"POW2": 0.3, "INT1": 0.2}),
            Skill("Piano", {"INT1": 0.3, "INT3": 0.2}),
            Skill("Math", {"INT3": 0.3, "SEN3": 0.2}),
        ]
        self.c1 = Charactor(
            "YUSHA",
            {
                "POW1": dice(2, 6),
                "POW2": dice(2, 6),
                "POW3": dice(2, 6),
                "SEN1": dice(2, 6),
                "SEN2": dice(2, 6),
                "SEN3": dice(2, 6),
                "INT1": dice(2, 6),
                "INT2": dice(2, 6),
                "INT3": dice(2, 6),

                "Swim": dice(2, 6),
                "Hit": dice(2, 6),
                "Piano": dice(2, 6),
                "Math": dice(2, 6),
            }
        )

    def test01(self, times):

        result = dict()
        for i in self.s:
            result[i.name] = list()

        print(self.c1.skills)

        for i in range(times):
            print(self.c1.name, end=' ')
            for j in self.s:
                answer = int(self.c1.getSP(j) * dice(2, 6))

                result[j.name].append(answer)
                if len(j.weight) != 0:
                    print('- {0} : {1:3}'.format(j.name, answer), end=' ')
            print()

        print("Avara", end=' ')
        for i in self.s:
            if len(i.weight) != 0:
                print('- {0} : {1:3}'.format(i.name, sum(result[i.name]) / len(result[i.name])), end=' ')
        print()


Test().test01(10)
