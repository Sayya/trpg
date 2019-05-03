from basemods import TrpgError

class Arbit:
    """ Role を受け取り、AIがその中の Thing を返す """

    @classmethod
    def order_next(self, role, desc, param):
        input('> ')
        if param.name not in role.ordered[desc].keys():
            role.ordered[desc][param.name] = role.order(param)

        try:
            rtn = next(role.ordered[desc][param.name])
        except StopIteration:
            role.ordered[desc][param.name] = role.order(param)
            rtn = next(role.ordered[desc][param.name])

        return rtn

    @classmethod
    def dialog(self, elem):
        return Arbit.inputa(list(elem.master.values()), 'Arbit', elem.__name__)

    @classmethod
    def dialg_propts(self, role, desc):
        try:
            rtn = Arbit.inputa(role.getpropts(), role.name, desc)
        except TrpgError as e:
            raise e
        
        return rtn

    @classmethod
    def dialg_propts2(self, role, desc):
        try:
            rtn1 = Arbit.dialg_propts(role, desc)
            if Arbit.inpute():
                rtn2 = Arbit.inputa(rtn1.getpropts(), rtn1.name, desc)
        except TrpgError as e:
            raise e
        
        return rtn2

    @classmethod
    def inputa(self, lis, name, desc):
        if len(lis) == 0:
            raise TrpgError('選択肢はありません')
        
        lis_disp = list()
        for i in lis:
            if hasattr(i, 'name'):
                lis_name = i.name
            else:
                lis_name = i.__name__
            lis_disp.append(lis_name)
        candi = dict(list(zip(list(range(len(lis))), lis_disp)))
        print('SELECT IN {0}'.format(candi))
        nam = input('[{0}]:{1} > '.format(name, desc))

        if nam not in [str(i) for i in candi.keys()]:
            raise TrpgError('選択しませんでした')

        return lis[int(nam)]

    @classmethod
    def inpute(self):
        rpl = ''
        exits = ('q', 'exit', 'quit')
        print('Exit IN {0}'.format(exits))
        rpl = input('選択を続けます > ')
        if rpl in exits:
            return False
        else:
            return True