from trpg import Dice, Param, Thing, Game

class Test:
    def __init__(self):
        Param('POW1', dict(), Dice(0,0))
        Param('POW2', dict(), Dice(0,0))
        Param('POW3', dict(), Dice(0,0))
        Param('SEN1', dict(), Dice(0,0))
        Param('SEN2', dict(), Dice(0,0))
        Param('SEN3', dict(), Dice(0,0))
        Param('INT1', dict(), Dice(0,0))
        Param('INT2', dict(), Dice(0,0))
        Param('INT3', dict(), Dice(0,0))

        Param('Swim', {'POW1': 0.1}, Dice(2,6))
        Param('Hit' , {'POW2': 0.3, 'INT1': 0.2}, Dice(3,5))
        Param('Piano', {'INT1': 0.3, 'INT3': 0.2}, Dice(4,4))
        Param('Math', {'INT3': 0.3, 'SEN3': 0.2}, Dice(5,3))

        d26 = Dice(2, 6).dice
        self.c1 = Thing(
            'YUSHA',
            {
                'POW1': d26(),
                'POW2': d26(),
                'POW3': d26(),
                'SEN1': d26(),
                'SEN2': d26(),
                'SEN3': d26(),
                'INT1': d26(),
                'INT2': d26(),
                'INT3': d26(),

                'Swim': d26(),
                'Hit' : d26(),
                'Piano': d26(),
                'Math': d26(),
            }
        )
        self.c2 = Thing(
            'DRAGO',
            {
                'POW1': d26(),
                'POW2': d26(),
                'POW3': d26(),
                'SEN1': d26(),
                'SEN2': d26(),
                'SEN3': d26(),
                'INT1': d26(),
                'INT2': d26(),
                'INT3': d26(),

                'Swim': d26(),
                'Hit' : d26(),
                'Piano': d26(),
                'Math': d26(),
            }
        )

    def test01(self, times):

        result = dict()
        for i in Param.master:
            result[i] = list()

        for i in range(times):
            for j in Param.master:
                answer = int(self.c1.dice(Param.master[j]))
                result[j].append(answer)

        print(self.c1.name, times, 'times Avarage', end=' ')
        for i in Param.master:
            if len(Param.master[i].weight) != 0:
                print('- {0} : {1:3}'.format(i, int(sum(result[i]) / len(result[i]))), end=' ')
        print()

        print(self.c1.name, end=' ')
        for i in Param.master:
            if len(Param.master[i].weight) != 0:
                print('- {0} : {1:3}'.format(i, self.c1.params[i]), end=' ')
        print()

        print(self.c2.name, end=' ')
        for i in Param.master:
            if len(Param.master[i].weight) != 0:
                print('- {0} : {1:3}'.format(i, self.c2.params[i]), end=' ')
        print()

    def test02(self, times):
        
        p, *_ = [ Param.master[i] for i in Param.master if i == 'Swim']
        g = Game(p)
        
        for i in range(times):
            print(
                'SUbject - {0:3} [VS] Object - {1:3}'.format(
                    int(g.point(self.c1)),
                    int(g.wall(self.c2)),
                ),
                end=' '
            )
            print('This [{0}]Game Result :'.format('Swim'), int(g.compare(self.c1, self.c2)))


Test().test01(10)
Test().test02(10)