from trpg import Dice, Param, Thing, Game

class Test:
    def __init__(self):
        self.s = [
            Param('POW1', dict(), Dice(0,0)),
            Param('POW2', dict(), Dice(0,0)),
            Param('POW3', dict(), Dice(0,0)),
            Param('SEN1', dict(), Dice(0,0)),
            Param('SEN2', dict(), Dice(0,0)),
            Param('SEN3', dict(), Dice(0,0)),
            Param('INT1', dict(), Dice(0,0)),
            Param('INT2', dict(), Dice(0,0)),
            Param('INT3', dict(), Dice(0,0)),

            Param('Swim', {'POW1': 0.1}, Dice(2,6)),
            Param('Hit' , {'POW2': 0.3, 'INT1': 0.2}, Dice(3,5)),
            Param('Piano', {'INT1': 0.3, 'INT3': 0.2}, Dice(4,4)),
            Param('Math', {'INT3': 0.3, 'SEN3': 0.2}, Dice(5,3)),
        ]
        self.c1 = Thing(
            'YUSHA',
            {
                'POW1': Dice(2, 6).dice(),
                'POW2': Dice(2, 6).dice(),
                'POW3': Dice(2, 6).dice(),
                'SEN1': Dice(2, 6).dice(),
                'SEN2': Dice(2, 6).dice(),
                'SEN3': Dice(2, 6).dice(),
                'INT1': Dice(2, 6).dice(),
                'INT2': Dice(2, 6).dice(),
                'INT3': Dice(2, 6).dice(),

                'Swim': Dice(2, 6).dice(),
                'Hit' : Dice(2, 6).dice(),
                'Piano': Dice(2, 6).dice(),
                'Math': Dice(2, 6).dice(),
            }
        )
        self.c2 = Thing(
            'DRAGO',
            {
                'POW1': Dice(2, 6).dice(),
                'POW2': Dice(2, 6).dice(),
                'POW3': Dice(2, 6).dice(),
                'SEN1': Dice(2, 6).dice(),
                'SEN2': Dice(2, 6).dice(),
                'SEN3': Dice(2, 6).dice(),
                'INT1': Dice(2, 6).dice(),
                'INT2': Dice(2, 6).dice(),
                'INT3': Dice(2, 6).dice(),

                'Swim': Dice(2, 6).dice(),
                'Hit' : Dice(2, 6).dice(),
                'Piano': Dice(2, 6).dice(),
                'Math': Dice(2, 6).dice(),
            }
        )

    def test01(self, times):

        result = dict()
        for i in self.s:
            result[i.name] = list()

        for i in range(times):
            for j in self.s:
                answer = int(self.c1.point(j))
                result[j.name].append(answer)

        print(self.c1.name, times, 'times Avarage', end=' ')
        for i in self.s:
            if len(i.weight) != 0:
                print('- {0} : {1:3}'.format(i.name, int(sum(result[i.name]) / len(result[i.name]))), end=' ')
        print()

        print(self.c1.name, end=' ')
        for i in self.s:
            if len(i.weight) != 0:
                print('- {0} : {1:3}'.format(i.name, self.c1.params[i.name]), end=' ')
        print()

        print(self.c2.name, end=' ')
        for i in self.s:
            if len(i.weight) != 0:
                print('- {0} : {1:3}'.format(i.name, self.c2.params[i.name]), end=' ')
        print()

    def test02(self, times):
        
        p, *_ = [ i for i in self.s if i.name == 'Swim']
        g = Game(p)
        
        for i in range(times):
            print(
                'SUbject - {0:3} [VS] Object - {1:3}'.format(
                    int(g.subject_point(self.c1)),
                    int(g.object_borderline(self.c2)),
                ),
                end=' '
            )
            print('This [{0}]Game Result :'.format('Swim'), int(g.compare()))


Test().test01(10)
Test().test02(10)