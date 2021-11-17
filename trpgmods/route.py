from basemods import TrpgError, Master, Dice
# from trpgmods import Event

class Route(Master):
    """
    ルーティング処理
    1. テキストによる状況説明
    2. 以下のうち一つか複数
    ・Processの繰り返し、中断（compare, fluctuate, next）
    ・Thingsの比較（compare）
    ・Thingの交換（xchange）
    ・Thingのパラム変更（vchange）

    ・生成（Product）
    """
    master = dict()
    pid = 0

    def __init__(self, \
        name:'str,名前', \
        route:'dict-0-Route.name:tuple-2-int,ルート'=dict(), \
        gevent:'Event.name,イベント'='', \
        prev:'int,初期値'=0, \
        noend:'bool,継続'=True, \
        group:'str,グループ'=''):

        super().__init__(name)
        self.route = route # {Route().name: (min, max)}
        self.gevent = gevent
        self.prev = prev
        self.noend = noend # Boolean
        self.group = group
        
        self.attrbuild()

    def attrbuild(self):
        self.next = self
        
    def buildvalid(self):
        # インポート部分
        from basemods import Holder
        from iotemp import Template
        
        for k in list(self.route.keys()): # delしているのでgeneratorでなくしてやる
            # int の Dice テンプレート処理 'xdy+z' - dict*tuple編
            lis_route = list(self.route[k])
            for i, v in zip(range(len(lis_route)), lis_route):
                if type(v) is str and v != 'next':
                    lis_route[i] = Dice.makedice(lis_route[i])
            self.route[k] = tuple(lis_route)

            # Route.name のテンプレート処理 - dict編
            if k not in Route.master.keys():
                value = self.route[k]
                del self.route[k]
                try:
                    tname = Template.holder[self.group][Route][k]
                    self.route[tname] = value
                except Exception:
                    print('TEMPLATEERROR: Route.route -{0}- k={1}, value={2}'.format(self.name, k, value))

        # Event.name のテンプレート処理 - scala編
        if self.gevent not in Holder.master('Event').keys():
            try:
                self.gevent = Template.holder[self.group][Holder.classt('Event')][self.gevent]
            except Exception:
                print('TEMPLATEERROR: Route.gevent -{0}-'.format(self.name))

        # int の Dice テンプレート処理 'xdy+z' - scala編
        if type(self.prev) is str:
            self.prev = Dice.makedice(self.prev)
        
    def event(self):
        # インポート部分
        from basemods import Holder
        
        if self.gevent == '' and self.name in Holder.master('Event').keys():
            return Holder.master('Event', self.name)
        elif self.gevent in Holder.master('Event').keys():
            return Holder.master('Event', self.gevent)
        
    def occur(self):
        def routing(n):
            """ ルーティングの設計 """
            for i in self.route.keys():
                # print('ルート情報 prev={0}, min={1}, max={2}'.format(n, self.route[i][0], self.route[i][1]))
                if self.route[i][0] == 'next' \
                or self.route[i][0] <= n < self.route[i][1] \
                or self.route[i][0] == n:
                    Route.master[i].prev = n
                    return Route.master[i]
            else:
                return self

        self.prev = self.event().do(self.prev)
        self.next = routing(self.prev)
        # print('Route next:', self.next.name)