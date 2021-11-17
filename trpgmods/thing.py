from basemods import TrpgError, Master, Dice
# from trpgmods import Param

class Thing(Master):
    """ 対象となるもの、オブジェクト """
    master = dict()
    pid = 0

    def __init__(self, \
        name:'str,名前', \
        params:'dict-0-Param.name:int,パラメータ'=dict(), \
        propts:'list-0-Thing.name,所有'=list(), \
        group:'str,グループ'=''):
        
        super().__init__(name)
        self.params = params
        self.propts = propts
        self.group = group

        self.attrbuild()

    def attrbuild(self):
        # [Thing()]
        self.f_compare = list()
        self.f_xchange = list()

        # パーセンテージ（HPなど）
        self.p_ratio = dict()
        for i in self.params.keys():
            self.p_ratio[i] = 1

        # 引数：対象のパラメータ
        self.point = lambda param: param.point(self.params)
        self.siz = lambda param: self.point(param) * param.ceil()
        self.bar = lambda param: self.siz(param) * self.p_ratio[param.name]
        
    def buildvalid(self):
        # インポート部分
        from basemods import Holder
        from iotemp import Template

        for k in list(self.params.keys()): # delしているのでgeneratorでなくしてやる
            # int の Dice テンプレート処理 'xdy+z' - dict編
            if type(self.params[k]) is str:
                self.params[k] = Dice.makedice(self.params[k])

            # Param.name のテンプレート処理 - dict編
            if k not in Holder.master('Param').keys():
                value = self.params[k]
                del self.params[k]
                try:
                    tname = Template.holder[self.group][Holder.classt('Param')][k]
                    self.params[tname] = value
                except Exception:
                    print('TEMPLATEERROR: Thing.params -{0}-'.format(self.name))

        # Thing.name のテンプレート処理 - list編
        for v in self.propts:
            if v not in Thing.master.keys():
                idx = self.propts.index(v)
                del self.propts[idx]
                try:
                    tname = Template.holder[self.group][Thing][v]
                    self.propts.insert(idx, tname)
                except Exception:
                    print('TEMPLATEERROR: Thing.propts -{0}-'.format(self.name))

    def getpropts(self):
        return [Thing.master[i] for i in self.propts]

    def fluctuate(self, param, n):
        self.p_ratio[param.name] = (self.bar(param) + n) / self.siz(param)
        return self.p_ratio[param.name]

    def change(self, param, n):
        self.params[param.name] += n
        return self.params[param.name]