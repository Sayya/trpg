from basemods import Master, Dice

class Param(Master):
    """ Thingの属性（パラメータ）になる """
    master = dict()
    pid = 0

    def __init__(self, \
        name:'str,名前', \
        weight:'dict-0-Param.name:int,重み'=dict(), \
        gdice:'tuple-2-int,ダイス'=(0, 0), \
        group:'str,グループ'=''):

        super().__init__(name)
        self.weight = weight # {Param().name: int}
        self.gdice = gdice
        self.group = group

        self.attrbuild()

    def attrbuild(self):
        # pointA: 重み(0 <= n <= 1)とパラメータ(Param.master[i])の数値を掛けたものの和
        self.pointA = lambda params: sum(Param.master[i].point(params) * self.weight[i] for i in self.weight.keys() if i != self.name)
        # pointB: 当クラスのパラメータ(params[self.name])の数値に重みを掛けた数値
        self.pointB = lambda params: params[self.name] * self.weight[self.name] if self.name in params else 0
        # pointAとpointBの和、pointAで遡って子Paramの重み計算が動的にできる
        # 引数：Thingの固有パラメータリスト
        # 戻値：数値
        self.point = lambda params: self.pointA(params) + self.pointB(params)

    def buildvalid(self):
        # インポート部分
        from iotemp import Template

        for k in list(self.weight.keys()): # delしているのでgeneratorでなくしてやる
            # int の Dice テンプレート処理 'xdy+z' - dict編
            if type(self.weight[k]) is str:
                self.weight[k] = Dice.makedice(self.weight[k])

            # Param.name のテンプレート処理 - dict編
            if k not in Param.master.keys():
                value = self.weight[k]
                del self.weight[k]
                try:
                    tname = Template.holder[self.group][Param][k]
                    self.weight[tname] = value
                except Exception:
                    print('TEMPLATEERROR: Param.weight -{0}-'.format(self.name))
                    
        # int の Dice テンプレート処理 'xdy+z' - tuple編
        for i, v in zip(range(len(self.gdice)), self.gdice):
            if type(v) is str:
                self.gdice[i] = Dice.makedice(self.gdice[i])
        
    def dice(self):
        return Dice(*self.gdice).dice()
    def ceil(self):
        return Dice(*self.gdice).ceil()
    def wall(self):
        return Dice(*self.gdice).wall()
    def flor(self):
        return Dice(*self.gdice).flor()