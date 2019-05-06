from basemods import TrpgError

class Holder:
    """ 仲介 """

    @classmethod
    def classt(self, elemname):
        import trpgmods

        if elemname not in ('Param', 'Thing', 'Process', 'Event', 'Route', 'Role'):
            raise TrpgError('{0} クラスはありません'.format(elemname))

        return getattr(trpgmods, elemname)

    @classmethod
    def master(self, elemname, objname=None):
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
    def buildvalid(self):
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
    def progr_out(self, iface):
        """
        ユーザに選択してもらう候補を出力
          OUT: {'curr_func': <func>, 'arg': (), 'next_func': <func>, 'multi_flag': 0/1}
          OUT: (lis, name, desc, multi_f)
        """
        Holder.iface = iface
        try:
            return Holder.iface['curr_func'](*Holder.iface['arg'])
        except TrpgError as e:
            raise e

    @classmethod
    def progr_in(self, rtn):
        """ 
          IN: 選択結果
          OUT: {'curr_func': <func>, 'arg': (), 'next_func': <func>, 'multi_flag': 0/1}
        """
        try:
            return Holder.iface['next_func'](rtn)
        except TrpgError as e:
            raise e