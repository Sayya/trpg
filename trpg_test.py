from trpg import Master, Dice, Param, Thing, Process, Event, Route, Role, Game
from iotemp import Template, Scenario

class Test:
    def __init__(self):

        Param('力', {'力': 1, })
        Param('感', {'感': 1, })
        Param('知', {'知': 1, })

        Param('戦', {'戦': 1, '力': 5, }, (2,6,10))
        Param('戦攻',  {'戦攻' : 0.5, '感': 4, }, (2,6))
        Param('戦防', {'戦防': 0.7, '知': 3, }, (2,6))

        Param('道', {'道': 1}, (1, 2))
        
        Thing('きびだんご', {'力': 1, '戦': 1, })
        Thing('きび単位', {'力': 1, '戦': 2, })

        Thing('桃', {'力': 10, '感': 10, '知': 10, '戦': 1, '戦攻': 1, '戦防': 1, }, ['きびだんご'])
        Thing('犬', {'力': 15, '感':  8, '知':  8, '戦': 1, '戦攻': 1, '戦防': 1, })
        Thing('雉', {'力':  8, '感': 15, '知':  8, '戦': 1, '戦攻': 1, '戦防': 1, })
        Thing('猿', {'力':  8, '感':  8, '知': 15, '戦': 1, '戦攻': 1, '戦防': 1, })

        d26 = Dice(2, 6).dice
        Thing('鬼A', {'力': 3, '感': 5, '知': 6, '戦': d26(), '戦攻': d26(), '戦防': d26(), })
        Thing('鬼B', {'力': 5, '感': 3, '知': 8, '戦': d26(), '戦攻': d26(), '戦防': d26(), })
        Thing('大鬼', {'力': 7, '感': 8, '知': 8, '戦': d26(), '戦攻': d26(), '戦防': d26(), })

        Process('Battle_Bar', '戦', 'bar')
        Process('Battle_COM', '戦', 'compare')
        Process('Battle_Inc', '戦', 'increase')
        Process('Battle_Dec', '戦', 'decrease', '戦攻', '戦防')

        Process('OneOfTwo', '道', 'dice')

        Event('1', text='むかしむかし、あるところに、おじいさんとおばあさんがいました。')
        Event('2', text='その日も、おじいさんは山へ芝刈りに、おばあさんは川へ洗濯に行っていました。')
        Event('3', text='おばあさんが川で洗濯をしていると、どんぶらこどんぶらこと大きな桃が流れてきました。')
        Event('4', text='- 中略 -')
        Event('12', text='桃太郎は鬼ヶ島へ鬼退治へと向かいました。')

        Event('R0', text='鬼ヶ島に来ている\nすると突然鬼が襲いかかってきた')
        Event('R1', 'Battle_COM', (0, 0, 1, 0), ('鬼A',''), text='鬼Aの攻撃\n誰が攻撃を受けますか？')
        Event('R1n', 'Battle_Dec', (0, 0, 0, 0), ('',''))
        Event('R2', 'Battle_COM', (0, 1, 0, 0), ('','鬼A'), text='桃太郎陣営の攻撃')
        Event('R2n', 'Battle_Dec', (0, 0, 0, 0), ('',''))
        Event('R3', text='さらに鬼が襲いかかってきた')
        Event('R4', 'Battle_COM', (0, 0, 1, 0), ('鬼B',''), text='鬼Bの攻撃\n誰が攻撃を受けますか？')
        Event('R4n', 'Battle_Dec', (0, 0, 0, 0), ('',''))
        Event('R5', 'Battle_COM', (0, 1, 0, 0), ('','鬼B'), text='桃太郎陣営の攻撃')
        Event('R5n', 'Battle_Dec', (0, 0, 0, 0), ('',''))
        Event('R6', 'OneOfTwo', text='何かが近づいてくる！？')
        Event('R7', text='大鬼が現れた')
        Event('R8', 'Battle_COM', (0, 0, 1, 0), ('大鬼',''), text='大鬼の攻撃\n誰が攻撃を受けますか？')
        Event('R8n', 'Battle_Dec', (0, 0, 0, 0), ('',''))
        Event('R9', 'Battle_COM', (0, 1, 0, 0), ('','大鬼'), text='桃太郎陣営の攻撃')
        Event('R9n', 'Battle_Dec', (0, 0, 0, 0), ('',''))
        Event('R10', text='大鬼は滅ぼされた\n故郷に平和が戻った')
        Event('gameover', text='ゲームオーバー')

        Event('RK0', 'Battle_Bar', (0, 0, 0, 0), ('','きびだんご'))
        Event('RK1', 'Battle_Inc', (0, 0, 1, 0), ('きびだんご',''))
        Event('RK2', 'Battle_Bar', (0, 0, 0, 0), ('きび単位','きびだんご'))

        Route('S', {'2': ('next', 0),}, '1')
        Route('2', {'3': ('next', 0),})
        Route('3', {'4': ('next', 0),})
        Route('4', {'12': ('next', 0),})
        Route('12', {'R1': ('next', 0),})

        Route('R0' , {'R1': (0, 0),})
        Route('R1' , {'R1n': ('next', 0),})
        Route('R1n', {'gameover': (0, 0),'R2': (1, 1000),})
        Route('R2' , {'R2n': ('next', 0),})
        Route('R2n', {'R3': (0, 0),'R1': (1, 1000),})
        Route('gameover', noend=False)
        Route('R3' , {'R4': (0, 0),}, noend=False)
        Route('R4' , {'R4n': ('next', 0),})
        Route('R4n', {'gameover': (0, 0),'R5': (1, 1000),})
        Route('R5' , {'R5n': ('next', 0),})
        Route('R5n', {'R6': (0, 0),'R4': (1, 1000),})
        Route('R6' , {'R7': (1, 0),'R6': (2, 0),})
        Route('R7' , {'R8': (0, 0),}, noend=False)
        Route('R8' , {'R8n': ('next', 0),})
        Route('R8n', {'gameover': (0, 0),'R9': (1, 1000),})
        Route('R9' , {'R9n': ('next', 0),})
        Route('R9n', {'R10': (0, 0),'R8': (1, 1000),})
        Route('R10', noend=False)
        
        Route('き', {'RK2': (-1000, 0), 'RK1': (1, 1000),}, 'RK0')
        Route('RK1', {'RK2': ('next', 0),})
        Route('RK2', {'き': ('next', 0),}, noend=False)

        Role('太郎', ['桃', '犬', '雉', '猿'], ['S', 'き'])

    def test01(self):
        Game(['太郎']).start()
        
Test().test01()
Test()
Scenario().wizard('Test')