from basemods import TrpgError, Master
# from trpgmods import Param

class Process(Master):
    """ Event の主処理 """
    master = dict()
    pid = 0

    def __init__(self, \
        name:'str,名前', \
        gtarget:'Param.name,主パラ'='', \
        gdeed:'Process.deed,処理'='', \
        gsbj_param:'Param.name,能パラ'='', \
        gobj_param:'Param.name,受パラ'='', \
        group:'str,グループ'=''):
        
        """
        deed option:
        - point, siz, bar
        - dice, ceil, wall, flor
        - vchange, xchange, compare, increase, decrease
        """
        
        super().__init__(name)
        self.gtarget = gtarget
        self.gdeed = gdeed # Event.deedの設定
        self.gsbj_param = gsbj_param
        self.gobj_param = gobj_param
        self.group = group
        
    def buildvalid(self):
        # インポート部分
        from basemods import Holder
        from iotemp import Template

        # Param.name のテンプレート処理 - scala編
        if self.gtarget not in Holder.master('Param').keys():
            try:
                self.gtarget = Template.holder[self.group][Holder.classt('Param')][self.gtarget]
            except Exception:
                print('TEMPLATEERROR: Process.gtarget -{0}-'.format(self.name))

        # Param.name のテンプレート処理 - scala編
        if self.gsbj_param not in Holder.master('Param').keys():
            try:
                self.gsbj_param = Template.holder[self.group][Holder.classt('Param')][self.gsbj_param]
            except Exception:
                print('TEMPLATEERROR: Process.gsbj_param -{0}-'.format(self.name))
                
        # Param.name のテンプレート処理 - scala編
        if self.gobj_param not in Holder.master('Param').keys():
            try:
                self.gobj_param = Template.holder[self.group][Holder.classt('Param')][self.gobj_param]
            except Exception:
                print('TEMPLATEERROR: Process.gobj_param -{0}-'.format(self.name))
    
    def target(self):
        # インポート部分
        from basemods import Holder

        return Holder.master('Param', self.gtarget)
    
    def sbj_param(self):
        # インポート部分
        from basemods import Holder
        
        return Holder.master('Param', self.gsbj_param)
    
    def obj_param(self):
        # インポート部分
        from basemods import Holder
        
        return Holder.master('Param', self.gobj_param)

    def deed(self, sbj, obj, n):
        try:
            return getattr(self, self.gdeed)(sbj, obj, n)
        except:
            return 0

    # Event.deed の拡張
    def point(self, sbj, obj, n):
        target = self.target()
        rtn = obj.point(target)

        print('{0} の -{1}- ポイントは {2}'.format(obj.name, target.name, rtn))
        return rtn

    def siz(self, sbj, obj, n):
        target = self.target()
        rtn = obj.siz(self.target())

        print('{0} の -{1}- 基準値は {2}'.format(obj.name, target.name, rtn))
        return rtn
    
    def bar(self, sbj, obj, n):
        target = self.target()
        rtn = obj.bar(self.target())

        print('{0} の -{1}- 変動値は {2}%'.format(obj.name, target.name, rtn))
        return rtn

    def dice(self, sbj, obj, n):
        target = self.target()
        rtn = target.dice()

        print('-{0}- は {1} になった'.format(target.name, rtn))
        return rtn
    
    def ceil(self, sbj, obj, n): return self.target().ceil()
    def wall(self, sbj, obj, n): return self.target().wall()
    def flor(self, sbj, obj, n): return self.target().flor()
    
    def reset(self, sbj, obj, n):
        target = self.target()
        r = obj.siz(target) - obj.bar(target)
        rtn = obj.fluctuate(target, 1 * r)

        print('{0} の -{1}- をリセットした'.format(obj.name, target.name))
        return rtn
    
    def vchange(self, sbj, obj, n):
        target = self.target()
        rtn = obj.change(target, sbj.point(target))

        print('{0} の -{1}- 値は {2}'.format(obj.name, target.name, rtn))
        return rtn

    # あるパラメータについて２つのThingにおける交換
    def xchange(self, sbj, obj, n):
        target = self.target()
        sbj_propts_target = [i for i in sbj.f_xchange if target.name in sbj.f_xchange[i].params]
        sbj_propts_nonget = [i for i in sbj.f_xchange if target.name not in sbj.f_xchange[i].params]
        obj_propts_target = [i for i in obj.f_xchange if target.name in obj.f_xchange[i].params]
        obj_propts_nonget = [i for i in obj.f_xchange if target.name not in obj.f_xchange[i].params]

        sbj.f_xchange = sbj_propts_nonget.extend(obj_propts_target)
        obj.f_xchange = obj_propts_nonget.extend(sbj_propts_target)

        return 1

    # あるパラメータについて２つのThingにおける差
    def compare(self, sbj, obj, n):
        target = self.target()
        sbj_propts_sum = sum(i.point(target) for i in sbj.f_compare if target.name in i.params) + 1
        obj_propts_sum = sum(i.point(target) for i in obj.f_compare if target.name in i.params) + 1
        
        offence = sbj.point(target) * sbj_propts_sum * target.dice() + sbj.point(self.sbj_param())
        defence = obj.point(target) * obj_propts_sum * target.dice() + obj.point(self.obj_param())

        rtn = offence - defence
        
        print('{0} の -{1}- は {2}'.format(sbj.name, target.name, int(rtn)))
        return rtn

    def increase(self, sbj, obj, n):
        """
        1. 比較し結果を得る
        2. 結果をもとにパラメータを変動させる
        3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
        """
        if n < 0:
            n = 0
        
        target = self.target()
        r = obj.fluctuate(target, 1 * n)
        
        print('{0} の -{1}- は {2}% になった'.format(obj.name, target.name, int(r * 100)))
        if r >= 1:
            return 1
        else:
            return 0

    def decrease(self, sbj, obj, n):
        """
        1. 比較し結果を得る
        2. 結果をもとにパラメータを変動させる
        3. パラメータの変動の結果、終了条件に適合すれば結果処理をする
        """
        if n < 0:
            n = 0
        
        target = self.target()
        r = obj.fluctuate(target, -1 * n)

        print('{0} の -{1}- は {2}% になった'.format(obj.name, target.name, int(r * 100)))
        if r <= 0:
            print('{0} はもう -{1}- できない'.format(obj.name, target.name))
            return 0
        else:
            return 1