from basemods import TrpgError

class Arbit:
    """ Role を受け取り、AIがその中の Thing を返す """

    nextmethod = lambda: None

    @classmethod
    def input_out(self, lis, name, desc):
        if len(lis) == 0:
            raise TrpgError('選択肢はありません')
        
        lis_disp = list()
        for i in lis:
            if hasattr(i, 'name'):
                lis_name = i.name
            elif hasattr(i, '__name__'):
                lis_name = i.__name__
            else:
                lis_name = repr(i)
            lis_disp.append(lis_name)
        candi = dict(list(zip(list(range(len(lis))), lis_disp)))

        return candi

    @classmethod
    def input_in(self, lis, candi, nam):
        if nam in [str(i) for i in candi.keys()]:
            return lis[int(nam)]
        else:
            return None