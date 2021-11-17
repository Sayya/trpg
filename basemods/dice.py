import random

class Dice:
    """ 2d6形式を表現できる乱数クラス """
    def __init__(self, times, maxim, offset=0):
        self.times = times
        self.maxim = maxim
        self.offset = offset

        # 戻値：数値
        self.dice = lambda: sum(random.randint(1, self.maxim) for i in range(self.times)) + self.offset

        self.ceil = lambda: self.times * self.maxim + self.offset
        self.wall = lambda: self.times * (self.maxim + 1) / 2 + self.offset
        self.flor = lambda: self.times * self.maxim + self.offset

    @classmethod
    def makedice(cls, form):
        """ 'xdy'/'xdy+z'形式なら Dice オブジェクトに変換 """
        if type(form) is str:
            times = 0
            maxim = 0
            offset = 0

            rslt = Dice.checkdice(form)
            if rslt == 1:
                # 'xdy+z'形式
                dice = form.split('d')
                modif = dice[1].split('+')

                times = int(dice[0])
                maxim = int(modif[0])
                offset = int(modif[1])
            elif rslt == 2:
                # 'xdy'形式
                dice = form.split('d')

                times = int(dice[0])
                maxim = int(dice[1])
            elif form.isdecimal():
                offset = int(form)
            
            return Dice(times, maxim, offset).dice()
        elif type(form) is int:
            return form
        else:
            return 0
            
    @classmethod
    def checkdice(cls, form):
        """ 'xdy'/'xdy+z'形式かどうかを判定 """
        rtn = 0
        
        dice = form.split('d')
        if len(dice) == 2 and dice[0].isdecimal():
            modif = dice[1].split('+')
            if len(modif) == 2 and modif[0].isdecimal() and modif[1].isdecimal():
                # 'xdy+z'形式
                rtn = 1
            elif len(modif) == 1 and dice[1].isdecimal():
                # 'xdy'形式
                rtn = 2
        
        return rtn