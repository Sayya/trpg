from basemods import TrpgError

class Holder:
    """ 仲介 """

    @classmethod
    def classt(cls, elemname):
        import trpgmods

        if elemname not in ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role'):
            raise TrpgError('{0} クラスはありません'.format(elemname))

        return getattr(trpgmods, elemname)

    @classmethod
    def master(cls, elemname, objname=None):
        import trpgmods

        if elemname not in ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role'):
            raise TrpgError('{0} クラスはありません'.format(elemname))
        
        if objname is None:
            return getattr(trpgmods, elemname).master
        elif objname in getattr(trpgmods, elemname).master.keys():
            return getattr(trpgmods, elemname).master[objname]
        else:
            raise TrpgError('{0} -{1}- はありません'.format(elemname, objname))

    @classmethod
    def buildvalid(cls):
        import trpgmods

        classts = ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role')

        for elemname in classts:
            classmaster = getattr(trpgmods, elemname).master
            for k, v in classmaster.items():
                try:
                    v.buildvalid()
                except TrpgError as e:
                    print('MESSAGE: {0}'.format(e.value))
                    print('VALIDATE: 削除 クラス -{0}- > アイテム -{1}-'.format(elemname, k))
                    del classmaster[k]
    
    @classmethod
    def progr_out(cls, iface):
        """
        ユーザに選択してもらう候補を出力
          IN: {'curr_func': <func>, 'arg': (), 'next_func': <func>, 'multi_flag': 0/1}
          OUT(wizard): (lis, desc, multi_f)
          OUT(plot)  : (lis, name, desc, multi_f)
        """
        Holder.iface = iface
        try:
            return Holder.iface['curr_func'](*Holder.iface['arg'])
        except TrpgError as e:
            raise e

    @classmethod
    def progr_in(cls, rtn):
        """ 
          IN: 選択結果
          OUT: {'curr_func': <func>, 'arg': (), 'next_func': <func>, 'multi_flag': 0/1}
        """
        try:
            next_func = Holder.iface['next_func']
            print('##### {0} <- ({1}) #####'.format(next_func.__name__, rtn))
            return Holder.iface['next_func'](rtn)
        except TrpgError as e:
            raise e