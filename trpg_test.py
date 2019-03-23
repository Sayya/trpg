from trpg import Master, Dice, Param, Thing, Process, Role, Event, Route, Game

class Test:
    def __init__(self):

        Param('POW', {'POW': 1, }, Dice(0,0))
        Param('SEN', {'SEN': 1, }, Dice(0,0))
        Param('INT', {'INT': 1, }, Dice(0,0))

        Param('戦', {'戦': 1, 'POW': 5, }, Dice(2,6,10))
        Param('Punch_Offence', {'Punch_Offence': 0.5, 'SEN': 4, }, Dice(2,6))
        Param('Punch_Deffence', {'Punch_Deffence': 0.7, 'INT': 3, }, Dice(2,6))
        
        Thing('きびだんご', {'戦': 1, }, list())
        Thing('きび単位', {'戦': 2, }, list())

        Thing('桃太郎', {'POW': 10, 'SEN': 10, 'INT': 10,
                       '戦': 1, 'Punch_Offence': 1, 'Punch_Deffence': 1, }, [Thing.master['きびだんご']])
        Thing('犬',  {'POW': 15, 'SEN': 8, 'INT':  8,
                       '戦': 1, 'Punch_Offence': 1, 'Punch_Deffence': 1, }, list())
        Thing('雉', {'POW': 8, 'SEN': 15, 'INT':  8,
                       '戦': 1, 'Punch_Offence': 1, 'Punch_Deffence': 1, }, list())
        Thing('猿', {'POW':  8, 'SEN':  8, 'INT': 15,
                       '戦': 1, 'Punch_Offence': 1, 'Punch_Deffence': 1, }, list())

        d26 = Dice(2, 6).dice
        Thing('鬼A', {'POW': 3, 'SEN': 5, 'INT': 6,
                        '戦': d26(), 'Punch_Offence': d26(), 'Punch_Deffence': d26(), }, list())
        Thing('鬼B', {'POW': d26(), 'SEN': d26(), 'INT': d26(),
                        '戦': d26(), 'Punch_Offence': d26(), 'Punch_Deffence': d26(), }, list())
        Thing('大鬼', {'POW': 30, 'SEN': 5, 'INT': 5,
                        '戦': d26(), 'Punch_Offence': d26(), 'Punch_Deffence': d26(), }, list())

        Process('Battle', Param.master['戦'], Param.master['Punch_Offence'], Param.master['Punch_Deffence'])

        Param('WAY', {'WAY': 1}, Dice(1, 2))
        Process('OneOfTwo', Param.master['WAY'], Param.master[''], Param.master[''])

        Event('K0', (None,Thing.master['きびだんご']), (Process.master['Battle'].bar, Process.master['Battle'].target), (0, 0, 0), '')
        Event('K1', (Thing.master['きびだんご'],None), (Process.master['Battle'].fluctuate_inc, Process.master[''].target), (0, 0, 1), '')
        Event('K2', (Thing.master['きび単位'],Thing.master['きびだんご']), (Process.master['Battle'].bar, Process.master['Battle'].target), (0, 0, 0), '')
        Route('kibidango', {'K1': (0, 0),}, True, Event.master['K0'])
        Route('K1', {'K2': (0, 0),}, True, Event.master['K1'])
        Route('K2', dict(), False, Event.master['K2'])

        Event('1', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), 'むかしむかし、あるところに、おじいさんとおばあさんがいました。')
        Event('2', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), 'その日も、おじいさんは山へ芝刈りに、おばあさんは川へ洗濯に行っていました。')
        Event('3', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), 'おばあさんが川で洗濯をしていると、どんぶらこどんぶらこと大きな桃が流れてきました。')
        Event('4', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), '- 中略 -')
        Event('5', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), '桃太郎はすくすくと育ち、あっという間に立派な青年に育ちました。')
        Event('6', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), 'そんな頃合いに、町の方で鬼どもが暴れまわっているという噂が聞こえてきました。')
        Event('7', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), '桃「おじいさん、僕、鬼退治をしに行くよ！」')
        Event('8', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), 'おじい「心優しい、桃太郎や。お前ならそういうと思って準備をしておいたよ」')
        Event('9', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), 'そう言っておいじいさんは桃太郎に刀と旗を渡しました。')
        Event('10', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), 'おばあ「お腹が空くといけないから、このきびだんごを持ってお行き」')
        Event('11', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), '桃「おばあさん、ありがとう。おばあさんのきびだんごは日本一ですから、食べれば力も百萬力です」')
        Event('12', (None,None), (Process.master[''].point, Process.master[''].target), (0, 1, 0), 'そう言って桃太郎は鬼ヶ島へ鬼退治へと向かいました。')
        Route('start', {'2': (0, 0),}, True, Event.master['1'])
        Route('2', {'3': (0, 0),}, True, Event.master['2'])
        Route('3', {'4': (0, 0),}, True, Event.master['3'])
        Route('4', {'5': (0, 0),}, True, Event.master['4'])
        Route('5', {'6': (0, 0),}, True, Event.master['5'])
        Route('6', {'7': (0, 0),}, True, Event.master['6'])
        Route('7', {'8': (0, 0),}, True, Event.master['7'])
        Route('8', {'9': (0, 0),}, True, Event.master['8'])
        Route('9', {'10': (0, 0),}, True, Event.master['9'])
        Route('10', {'11': (0, 0),}, True, Event.master['10'])
        Route('11', {'12': (0, 0),}, True, Event.master['11'])
        Route('12', {'R1': (0, 0),}, True, Event.master['12'])

        Event('E0', (None,None), (Process.master[''].point, Process.master[''].target), (0, 0, 0), '鬼ヶ島に来ている\nすると突然鬼が襲いかかってきた')
        Event('E1', (Thing.master['鬼A'],None), (Process.master['Battle'].fluctuate_dec, Process.master['Battle'].target), (0, 0, 1), '鬼Aの攻撃\n誰が攻撃を受けますか？')
        Event('E2', (None,Thing.master['鬼A']), (Process.master['Battle'].fluctuate_dec, Process.master['Battle'].target), (0, 1, 0), '桃太郎陣営の攻撃')
        Event('E3', (None,None), (Process.master[''].point, Process.master[''].target), (0, 0, 0), 'さらに鬼が襲いかかってきた')
        Event('E4', (Thing.master['鬼B'],None), (Process.master['Battle'].fluctuate_dec, Process.master['Battle'].target), (0, 0, 1), '鬼Bの攻撃\n誰が攻撃を受けますか？')
        Event('E5', (None,Thing.master['鬼B']), (Process.master['Battle'].fluctuate_dec, Process.master['Battle'].target), (0, 1, 0), '桃太郎陣営の攻撃')
        Event('E6', (None,None), (Process.master['OneOfTwo'].dice, Process.master['OneOfTwo'].target), (0, 1, 0), '何かが近づいてくる！？')
        Event('E7', (None,None), (Process.master[''].point, Process.master[''].target), (0, 0, 0), '大鬼が現れた')
        Event('E8', (Thing.master['大鬼'],None), (Process.master['Battle'].fluctuate_dec, Process.master['Battle'].target), (0, 0, 1), '大鬼の攻撃\n誰が攻撃を受けますか？')
        Event('E9', (None,Thing.master['大鬼']), (Process.master['Battle'].fluctuate_dec, Process.master['Battle'].target), (0, 1, 0), '桃太郎陣営の攻撃')
        Event('E10', (None,None), (Process.master[''].point, Process.master[''].target), (0, 0, 0), '大鬼は滅ぼされた\n故郷に平和が戻った')
        Event('gameover', (None,None), (Process.master[''].point, Process.master[''].target), (0, 0, 0), 'ゲームオーバー')

        Route('R0', {'R1': (0, 0),}, True, Event.master['E0'])
        Route('R1', {'gameover': (0, 0),'R2': (1, 1000),}, True, Event.master['E1'])
        Route('R2', {'R3': (0, 0),'R1': (1, 1000),}, True, Event.master['E2'])
        Route('gameover', dict(), False, Event.master['gameover'])
        Route('R3', {'R4': (0, 0),}, False, Event.master['E3'])
        Route('R4', {'gameover': (0, 0),'R5': (1, 1000),}, True, Event.master['E4'])
        Route('R5', {'R6': (0, 0),'R4': (1, 1000),}, True, Event.master['E5'])
        Route('R6', {'R7': (1, 0),'R6': (2, 0),}, True, Event.master['E6'])
        Route('R7', {'R8': (0, 0),}, False, Event.master['E7'])
        Route('R8', {'gameover': (0, 0),'R9': (1, 1000),}, True, Event.master['E8'])
        Route('R9', {'R10': (0, 0),'R8': (1, 1000),}, True, Event.master['E9'])
        Route('R10', dict(), False, Event.master['E10'])

        Role('TARO', [Thing.master['桃太郎'], Thing.master['犬'], Thing.master['雉'], Thing.master['猿']], [Route.master['start'], Route.master['kibidango']])

    def test01(self):
        Game([Role.master['TARO']]).start()
        
Test().test01()