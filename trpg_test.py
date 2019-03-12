from trpg import Dice, Param, Thing, Process, Event, Game

class Test:
    def __init__(self):
        Param('POW', {'POW': 1}, Dice(0,0))
        Param('SEN', {'SEN': 1}, Dice(0,0))
        Param('INT', {'INT': 1}, Dice(0,0))

        Param('Limb', {'Limb': 1, 'POW': 0.5, 'SEN': 0.2}, Dice(2,6))
        Param('Body', {'Body': 1, 'POW': 0.3, 'INT': 0.4}, Dice(2,6))

        Param('Punch', {'Punch': 1, 'Limb': 0.3, 'Body': 0.2}, Dice(2,6))
        Param('Punch_Offence', {'Punch_Offence': 0.1, 'Limb': 0.5}, Dice(2,6))
        Param('Punch_Deffence', {'Punch_Deffence': 1, 'Body': 0.5}, Dice(2,6))

        self.p1 = Process('Battle',
            Param.master['Punch'],
            Param.master['Punch_Offence'],
            Param.master['Punch_Deffence'],
        )

        d26 = Dice(2, 6).dice
        self.c1 = Thing(
            'YUSHA',
            {
                'POW': d26(),
                'SEN': d26(),
                'INT': d26(),

                'Limb': d26(),
                'Body': d26(),

                'Punch': d26(),
                'Punch_Offence': d26(),
                'Punch_Deffence': d26(),
            },
            dict(),
        )
        self.c2 = Thing(
            'DRAGO',
            {
                'POW': d26(),
                'SEN': d26(),
                'INT': d26(),

                'Limb': d26(),
                'Body': d26(),

                'Punch': d26(),
                'Punch_Offence': d26(),
                'Punch_Deffence': d26(),
            },
            dict(),
        )

        self.e1 = Event(
            'Event1',
            {
                'Event2': 3,
                'Event3': 5,
            },
            self.p1.next,
            True,
        )

        self.e1 = Event(
            'Event2',
            {
                'Event1': 2,
                'Event3': 5,
            },
            print,
            True,
        )

        self.e1 = Event(
            'Event3',
            dict(),
            print,
            False,
        )

    def test01(self, times):
        """times回数の平均Param値を算出"""

        result = dict()
        for i in Param.master:
            result[i] = list()

        for i in range(times):
            for j in Param.master:
                answer = int(self.c1.point(Param.master[j]) * Param.master[j].dice())
                result[j].append(answer)

        print(self.c1.name, times, 'times Avarage', end=' ')
        for i in Param.master:
            if len(Param.master[i].weight) != 0:
                print('- {0} : {1:3}'.format(i, int(sum(result[i]) / len(result[i]))), end=' ')
        print()

        print(self.c1.name, end=' ')
        for i in Param.master:
            if len(Param.master[i].weight) != 0:
                if i in self.c1.params:
                   print('- {0} : {1:3}'.format(i, self.c1.params[i]), end=' ')
        print()

        print(self.c2.name, end=' ')
        for i in Param.master:
            if len(Param.master[i].weight) != 0:
                if i in self.c2.params:
                   print('- {0} : {1:3}'.format(i, self.c2.params[i]), end=' ')
        print()
        print()


    def test02(self, times):
        """times回数Process.compare()を出力する"""
        m = Process.master['Battle']
        
        for i in range(times):
            print('This [{0}]Game Result :'.format('Battle'), int(m.compare(self.c1, self.c2)))
        print()

    def test03(self):
        """一回のProcess.next()の調査"""

        print(self.c1.name, 'WALL:', int(self.c1.point(self.p1.target)))
        print(self.c2.name, 'MAX HP:', int(self.c2.bar(self.p1.target)))
        print()

        n = self.p1.compare(self.c1, self.c2)
        if n < 0:
            n = 0
        r = self.p1.fluctuate(self.c2, -1 * n)
        b = self.p1.next(r)

        print(self.p1.name, 'damage:',  int(n))
        print(self.c2.name, 'HP:', int(self.c2.bar(self.p1.target)))
        print(self.c2.name, 'ratio:', int(r * 100), '%')
        print('result:', b)
        print()
    
    def test04(self):
        pass


Test().test01(10)
#Test().test02(1)
Test().test03()