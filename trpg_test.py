from trpg import Master, Dice, Param, Thing, Process, Role, Event, Route, Game

class Test:
    def __init__(self):
        Param('WAY', {'WAY': 1}, Dice(1, 2))

        Param('POW', {'POW': 1}, Dice(0,0))
        Param('SEN', {'SEN': 1}, Dice(0,0))
        Param('INT', {'INT': 1}, Dice(0,0))

        Param('Limb', {'Limb': 1, 'POW': 0.5, 'SEN': 0.2}, Dice(2,6))
        Param('Body', {'Body': 1, 'POW': 0.3, 'INT': 0.4}, Dice(2,6))

        Param('Punch', {'Punch': 1, 'Limb': 0.3, 'Body': 0.2}, Dice(2,6))
        Param('Punch_Offence', {'Punch_Offence': 0.1, 'Limb': 0.5}, Dice(2,6))
        Param('Punch_Deffence', {'Punch_Deffence': 1, 'Body': 0.5}, Dice(2,6))

        Thing('momo', {'POW': 10, 'SEN': 10, 'INT': 10, 'Limb': 10, 'Body': 10,
                       'Punch': 10, 'Punch_Offence': 10, 'Punch_Deffence': 10,}, list())
        Thing('inu',  {'POW': 10, 'SEN': 12, 'INT':  5, 'Limb':  5, 'Body': 15,
                       'Punch': 10, 'Punch_Offence': 10, 'Punch_Deffence': 10,}, list())
        Thing('kiji', {'POW': 12, 'SEN': 15, 'INT':  3, 'Limb': 10, 'Body': 15,
                       'Punch': 10, 'Punch_Offence': 10, 'Punch_Deffence': 10,}, list())
        Thing('saru', {'POW':  5, 'SEN':  5, 'INT': 20, 'Limb': 10, 'Body': 15,
                       'Punch': 10, 'Punch_Offence': 10, 'Punch_Deffence': 10,}, list())

        d26 = Dice(2, 6).dice
        Thing('ONI_A', {'POW': d26(), 'SEN': d26(), 'INT': d26(), 'Limb': d26(),
                        'Punch': d26(), 'Punch_Offence': d26(), 'Punch_Deffence': d26(),}, list())
        Thing('ONI_B', {'POW': d26(), 'SEN': d26(), 'INT': d26(), 'Limb': d26(),
                        'Punch': d26(), 'Punch_Offence': d26(), 'Punch_Deffence': d26(),}, list())
        Thing('ONIGA', {'POW': 30, 'SEN': 5, 'INT': 5, 'Limb': 5, 'Body': 10,
                        'Punch': d26(), 'Punch_Offence': d26(), 'Punch_Deffence': d26(),}, list())

        Process('Battle', Param.master['Punch'], Param.master['Punch_Offence'], Param.master['Punch_Deffence'])
        Process('OneOfTwo', Param.master['WAY'], Param.master[''], Param.master[''])

        Event('E0', (None,None), (Process.master[''].point, Process.master[''].target), (0, 0, 0, 0), 'プレーヤを選んでください')
        Event('E1', (None,Thing.master['ONI_A']), (Process.master['Battle'].fluctuate, Process.master['Battle'].target), (0, 1, 0, 0), '君は鬼ヶ島に来ている\n鬼が現れた')
        Event('E2', (None,Thing.master['ONI_B']), (Process.master['Battle'].fluctuate, Process.master['Battle'].target), (0, 1, 0, 0), '君は鬼ヶ島に来ている\nさらに鬼が現れた')
        Event('E3', (None,None), (Process.master['OneOfTwo'].dice, Process.master['OneOfTwo'].target), (0, 0, 0, 0), '何かが近づいてくる！？')
        Event('E4', (None,Thing.master['ONIGA']), (Process.master['Battle'].fluctuate, Process.master['Battle'].target), (0, 1, 0, 0), '鬼の王が現れた')
        Event('E5', (None,None), (Process.master[''].point, Process.master[''].target), (0, 0, 0, 0), '鬼の王は滅ぼされた\n故郷に平和が戻った')

        Route('R0', {'R1': (0, 0),}, True, Event.master['E0'])
        Route('R1', {'R2': (0, 0),}, True, Event.master['E1'])
        Route('R2', {'R3': (0, 0),}, True, Event.master['E2'])
        Route('R3', {'R1': (1, 0), 'R4': (2, 0),}, False, Event.master['E3'])
        Route('R4', {'R5': (0, 0),}, True, Event.master['E4'])
        Route('R5', dict(), False, Event.master['E5'])

        Role('TARO', [Thing.master['momo'], Thing.master['inu'], Thing.master['kiji'], Thing.master['saru']], [Route.master['R0']])

    def test01(self, times):
        """times回数の平均Param値を算出"""
        pass

    def test02(self, times):
        """times回数Process.compare()を出力する"""
        pass

    def test03(self):
        """一回のProcess.next()の調査"""
        pass
    
    def test04(self):
        """お逃しません"""
        Game([Role.master['TARO']]).start()

#Test().test01(10)
#Test().test02(1)
#Test().test03()
Test().test04()