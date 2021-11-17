from basemods import TrpgError, Arbit, Holder
from iotemp import Template

class Test:
    def __init__(self):
        # インポート部分
        from trpgmods import Param, Thing, Process, Event, Route, Role

        Template(Param).make('力', {'力': 1, })
        Template(Param).make('感', {'感': 1, })
        Template(Param).make('知', {'知': 1, })

        Template(Param).make('戦', {'戦': 1, '力': 5, }, (2,6,10))
        Template(Param).make('戦攻',  {'戦攻' : 0.5, '感': 4, }, (2,6))
        Template(Param).make('戦防', {'戦防': 0.7, '知': 3, }, (2,6))

        Template(Param).make('道', {'道': 1}, (1, 2))
        
        Template(Thing).make('きびだんご', {'力': 1, '戦': 1, })
        Template(Thing).make('きび単位', {'力': 1, '戦': 2, })

        Template(Thing).make('桃', {'力': 10, '感': 10, '知': 10, '戦': 1, '戦攻': 1, '戦防': 1, }, ['きびだんご'])
        Template(Thing).make('犬', {'力': 15, '感':  8, '知':  8, '戦': 1, '戦攻': 1, '戦防': 1, })
        Template(Thing).make('雉', {'力':  8, '感': 15, '知':  8, '戦': 1, '戦攻': 1, '戦防': 1, })
        Template(Thing).make('猿', {'力':  8, '感':  8, '知': 15, '戦': 1, '戦攻': 1, '戦防': 1, })

        Template(Thing).make('鬼A', {'力': 6, '感': 5, '知': '2d6+5', '戦': '2d3+8', })
        Template(Thing).make('鬼B', {'力': 8, '感': 3, '知': '2d6+5', '戦': '2d3+10', })
        Template(Thing).make('大鬼', {'力': 10, '感': 8, '知': '2d6+5', '戦': '2d3+15', })

        Template(Process).make('Battle_Bar', '戦', 'bar')
        Template(Process).make('Battle_COM', '戦', 'compare')
        Template(Process).make('Battle_Inc', '戦', 'increase')
        Template(Process).make('Battle_Dec', '戦', 'decrease', '戦攻', '戦防')

        Template(Process).make('OneOfTwo', '道', 'dice')

        Template(Event).make('1', text='むかしむかし、あるところに、おじいさんとおばあさんがいました。')
        Template(Event).make('2', text='その日も、おじいさんは山へ芝刈りに、おばあさんは川へ洗濯に行っていました。')
        Template(Event).make('3', text='おばあさんが川で洗濯をしていると、どんぶらこどんぶらこと大きな桃が流れてきました。')
        Template(Event).make('4', text='- 中略 -')
        Template(Event).make('12', text='桃太郎は鬼ヶ島へ鬼退治へと向かいました。')

        Template(Event).make('R0', text='鬼ヶ島に来ている\nすると突然鬼が襲いかかってきた')
        Template(Event).make('R1', 'Battle_COM', (0, 0, 1, 0), ('鬼島','太郎'), ('鬼A',''), text='鬼Aの攻撃\n誰が攻撃を受けますか？')
        Template(Event).make('R1n', 'Battle_Dec', (0, 0, 0, 0), ('鬼島','太郎'), ('',''))
        Template(Event).make('R2', 'Battle_COM', (0, 3, 0, 0), ('太郎','鬼島'), ('','鬼A'), text='桃太郎陣営の攻撃')
        Template(Event).make('R2n', 'Battle_Dec', (0, 0, 0, 0), ('太郎','鬼島'), ('',''))
        Template(Event).make('R3', text='さらに鬼が襲いかかってきた')
        Template(Event).make('R4', 'Battle_COM', (0, 0, 1, 0), ('鬼島','太郎'), ('鬼B',''), text='鬼Bの攻撃\n誰が攻撃を受けますか？')
        Template(Event).make('R4n', 'Battle_Dec', (0, 0, 0, 0), ('鬼島','太郎'), ('',''))
        Template(Event).make('R5', 'Battle_COM', (0, 3, 0, 0), ('太郎','鬼島'), ('','鬼B'), text='桃太郎陣営の攻撃')
        Template(Event).make('R5n', 'Battle_Dec', (0, 0, 0, 0), ('太郎','鬼島'), ('',''))
        Template(Event).make('R6', 'OneOfTwo', text='何かが近づいてくる！？')
        Template(Event).make('R7', text='大鬼が現れた')
        Template(Event).make('R8', 'Battle_COM', (0, 0, 1, 0), ('鬼島','太郎'), ('大鬼',''), text='大鬼の攻撃\n誰が攻撃を受けますか？')
        Template(Event).make('R8n', 'Battle_Dec', (0, 0, 0, 0), ('鬼島','太郎'), ('',''))
        Template(Event).make('R9', 'Battle_COM', (0, 3, 0, 0), ('太郎','鬼島'), ('','大鬼'), text='桃太郎陣営の攻撃')
        Template(Event).make('R9n', 'Battle_Dec', (0, 0, 0, 0), ('太郎','鬼島'), ('',''))
        Template(Event).make('R10', text='大鬼は滅ぼされた\n故郷に平和が戻った')
        Template(Event).make('gameover', text='ゲームオーバー')

        Template(Event).make('RK0', 'Battle_Bar', (0, 0, 0, 0), ('',''), ('','きびだんご'))
        Template(Event).make('RK1', 'Battle_Inc', (0, 0, 1, 0), ('',''), ('きびだんご',''))
        Template(Event).make('RK2', 'Battle_Bar', (0, 0, 0, 0), ('',''), ('きび単位','きびだんご'))

        Template(Route).make('S', {'2': ('next', 0),}, '1')
        Template(Route).make('2', {'3': ('next', 0),})
        Template(Route).make('3', {'4': ('next', 0),})
        Template(Route).make('4', {'12': ('next', 0),})
        Template(Route).make('12', {'R1': ('next', 0),})

        Template(Route).make('R0' , {'R1': (0, 0),})
        Template(Route).make('R1' , {'R1n': ('next', 0),})
        Template(Route).make('R1n', {'gameover': (0, 0),'R2': (1, 1000),})
        Template(Route).make('R2' , {'R2n': ('next', 0),})
        Template(Route).make('R2n', {'R3': (0, 0),'R1': (1, 1000),})
        Template(Route).make('gameover', noend=False)
        Template(Route).make('R3' , {'R4': (0, 0),}, noend=False)
        Template(Route).make('R4' , {'R4n': ('next', 0),})
        Template(Route).make('R4n', {'gameover': (0, 0),'R5': (1, 1000),})
        Template(Route).make('R5' , {'R5n': ('next', 0),})
        Template(Route).make('R5n', {'R6': (0, 0),'R4': (1, 1000),})
        Template(Route).make('R6' , {'R7': (1, 0),'R6': (2, 0),})
        Template(Route).make('R7' , {'R8': (0, 0),}, noend=False)
        Template(Route).make('R8' , {'R8n': ('next', 0),})
        Template(Route).make('R8n', {'gameover': (0, 0),'R9': (1, 1000),})
        Template(Route).make('R9' , {'R9n': ('next', 0),})
        Template(Route).make('R9n', {'R10': (0, 0),'R8': (1, 1000),})
        Template(Route).make('R10', noend=False)
        
        Template(Route).make('き', {'RK2': (-1000, 0), 'RK1': (1, 1000),}, 'RK0')
        Template(Route).make('RK1', {'RK2': ('next', 0),})
        Template(Route).make('RK2', {'き': ('next', 0),}, noend=False)

        Template(Role).make('太郎', ['桃', '犬', '雉', '猿'], ['S', 'き'])
        Template(Role).make('鬼島', ['鬼A', '鬼B', '大鬼'])
        
if __name__ == '__main__':
    
    # インポート部分
    from iotemp import Scenario
    from game import Game

    __package__ = 'trpg'
    print('__package__: {}, __name__: {}'.format(__package__, __name__))

    Test()
    Game(['太郎'])

    while True:
        print('SELECT IN {0}'.format({0: 'wizard', 1: 'game'}))
        start = input('> ')

#        try:
        if start == '0':
            s_argdic = Scenario.argdic_first()
            while True:
                wiz_out = Holder.progr_out(s_argdic)

                if wiz_out[2] is None:
                    break

                try:
                    if not wiz_out[2]:
                        # 自由に入力
                        if wiz_out[0] is None:
                            raise TrpgError('選択肢しませんでした')
                        print('UPDATE IN {0}'.format(wiz_out[0]))
                        wiz_in = input('{0} > '.format(wiz_out[1]))
                    else:
                        # リストからの選択
                        s_candi = Arbit.input_out(wiz_out[0], 'Scenario', 'make')
                        print('SELECT IN {0}'.format(s_candi))
                        nam = input('{0} > '.format(wiz_out[1]))
                        wiz_in = Arbit.input_in(wiz_out[0], s_candi, nam)
                except TrpgError as e:
                    # print('MESSAGE: {0}'.format(e.value))
                    pass
                except Exception as e:
                    print('ERROR: {0}'.format(e))
                    pass
                s_argdic = Holder.progr_in(wiz_in)
        else:
            g_argdic = Game.argdic_first()
            while True:
                rtn_out = Holder.progr_out(g_argdic)

                if rtn_out[3] is None:
                    break

                try:
                    g_candi = Arbit.input_out(*rtn_out[:3])
                    if rtn_out[3]: # 複数の場合 list に
                        nam = list()
                        while True:
                            print('SELECT IN {0}'.format(g_candi))
                            rslt = input('[{0}]:{1} > '.format(rtn_out[1], rtn_out[2]))
                            if rslt in ('q', 'quit', 'exit'):
                                break
                            nam.append(rslt)
                        rtn_in = [Arbit.input_in(rtn_out[0], g_candi, i) for i in nam]
                    else:
                        print('SELECT IN {0}'.format(g_candi))
                        nam = input('[{0}]:{1} > '.format(rtn_out[1], rtn_out[2]))
                        rtn_in = Arbit.input_in(rtn_out[0], g_candi, nam)
                except TrpgError as e:
                    # print('Error: {0}'.format(e.value))
                    pass
                except Exception as e:
                    print('ERROR: {0}'.format(e))
                    pass
                g_argdic = Holder.progr_in(rtn_in)
#        except Exception as e:
#            print('ERROR: {0}'.format(e))
#            pass

# trpg ディレクトリの一つ上の階層で以下のコマンド
# > python -m trpg.test