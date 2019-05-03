from basemods import TrpgError, Master, Arbit
# from trpgmods import Thing, Process, Role

class Event(Master):
    """ イベント """
    master = dict()
    pid = 0

    def __init__(self, \
        name:'str,名前', \
        procs:'Process.name,プロセス'='', \
        rolething_f:'tuple-4-int,(ロールフラグ;能動フラグ;受動フラグ;文字送り)'=(0, 0, 0, 1), \
        role:'tuple-2-Role.name,(能動ロール;受動ロール)'=('',''), \
        thing:'tuple-2-Thing.name,(能動者;受動者)'=('',''), \
        text:'str,テキスト'='', \
        group:'str,グループ'=''):
        
        """
        ロールフラグ: 0 = デフォ, 1 = 能動者のみ, 2 = 受動者のみ, 3 = 両方
        能動受動フラグ: 0 = 選択なし, 1 = 単選択, 2 = 所有選択, 3 = 順選択
        文字送り: 0 = しない, 1 = する
        """
        
        super().__init__(name)
        self.procs = procs
        self.rolething_f = rolething_f
        self.role = role
        self.thing = thing
        self.text = text
        self.group = group
        
        self.attrbuild()

    def attrbuild(self):
        # インポート部分
        from basemods import Holder

        self.target = Holder.master('Process', self.procs).target()
        self.sbj = Holder.master('Thing', '')
        self.obj = Holder.master('Thing', '')
        
    def buildvalid(self):
        # インポート部分
        from basemods import Holder
        from iotemp import Template

        # Process.name のテンプレート処理 - scala編
        if self.procs not in Holder.master('Process').keys():
            try:
                self.procs = Template.holder[self.group][Holder.classt('Process')][self.procs]
            except Exception:
                print('TEMPLATEERROR: Event.procs')
                
        lis_role = list(self.role)
        for v in lis_role:
            # Role.name のテンプレート処理 - tuple編
            if v not in Holder.master('Role').keys():
                idx = lis_role.index(v)
                del lis_role[idx]
                try:
                    tname1 = Template.holder[self.group][Holder.classt('Role')][v]
                except Exception:
                    tname1 = ''
                    print('TEMPLATEERROR: Event.role -{0}- v={1}, idx={2}'.format(self.name, v, idx))
                lis_role.insert(idx, tname1)
        self.role = tuple(lis_role)

        lis_thing = list(self.thing)
        for v in lis_thing:
            # Thing.name のテンプレート処理 - tuple編
            if v not in Holder.master('Thing').keys():
                idx = lis_thing.index(v)
                del lis_thing[idx]
                try:
                    tname2 = Template.holder[self.group][Holder.classt('Thing')][v]
                except Exception:
                    tname2 = ''
                    print('TEMPLATEERROR: Event.thing -{0}- v={1}, idx={2}'.format(self.name, v, idx))
                lis_thing.insert(idx, tname2)
        self.thing = tuple(lis_thing)
        
        if len(self.role) != 2:
            raise TrpgError('引数 -{0}- のリストサイズが２ではありません'.format('role'))        
        if len(self.thing) != 2:
            raise TrpgError('引数 -{0}- のリストサイズが２ではありません'.format('thing'))
    
    def role_f(self):
        return self.rolething_f[0]
        
    def sbj_f(self):
        return self.rolething_f[1]
        
    def obj_f(self):
        return self.rolething_f[2]
        
    def cap_f(self):
        return self.rolething_f[3]

    def sbjrole_m_str(self):
        return self.role[0]

    def objrole_m_str(self):
        return self.role[1]

    def sbjthing_m(self):
        # インポート部分
        from basemods import Holder

        return Holder.master('Thing', self.thing[0])

    def objthing_m(self):
        # インポート部分
        from basemods import Holder

        return Holder.master('Thing', self.thing[1])
    
    def do(self, n):
        # インポート部分
        from basemods import Holder

        return Holder.master('Process', self.procs).deed(self.sbj, self.obj, n)

    def focus(self, role):
        from trpgmods import Role

        role_f = self.role_f()
        sbj_f = self.sbj_f()
        obj_f = self.obj_f()
        cap_f = self.cap_f()

        sbjrole_m_str = self.sbjrole_m_str()
        sbjthing_m = self.sbjthing_m()
        objrole_m_str = self.objrole_m_str()
        objthing_m = self.objthing_m()

        role_first = role
        
        if self.text != '':
            print(self.text)
            
        #文字送りで入力なし
        if cap_f == 1:
            input('> ')
            return

        # 能動ロールの設定
        if sbjrole_m_str == '':
            try:
                if role_f == 1 or role_f == 3:
                    role = Arbit.dialog(Role)
            except TrpgError as e:
                print('MESSAGE: ', e.value)
                role = role_first
        else:
            role = Role.master[sbjrole_m_str]

        # 能動者の設定
        if sbjthing_m.name == '':
            if role.sbj.name == '':
                self.sbj = role.getpropts()[0]
            else:
                self.sbj = role.sbj
            # print('Role -{0}- のデフォルト能動者 -{1}-'.format(role.name, self.sbj.name))

            try:
                if sbj_f == 1:
                    self.sbj = Arbit.dialg_propts(role, 'sbj')
                    role.sbj = self.sbj
                elif sbj_f == 2:
                    self.sbj = Arbit.dialg_propts2(role, 'sbj')
                    role.sbj = self.sbj
                elif sbj_f == 3:
                    self.sbj = Arbit.order_next(role, 'sbj', self.target)
                    role.sbj = self.sbj
            except TrpgError as e:
                print('MESSAGE: ', e.value)
                role.sbj = self.sbj
        else:
            self.sbj = sbjthing_m
            role.sbj = self.sbj

        # 受動ロールの設定
        if objrole_m_str == '':
            try:
                if role_f == 2 or role_f == 3:
                    role = Arbit.dialog(Role)
            except TrpgError as e:
                print('MESSAGE: ', e.value)
                role = role_first
        else:
            role = Role.master[objrole_m_str]

        # 受動者の設定
        if objthing_m.name == '':
            if role.obj.name == '':
                self.obj = role.getpropts()[0]
            else:
                self.obj = role.obj
            # print('Role -{0}- のデフォルト受動者 -{1}-'.format(role.name, self.obj.name))

            try:
                if obj_f == 1:
                    self.obj = Arbit.dialg_propts(role, 'obj')
                    role.obj = self.obj
                elif obj_f == 2:
                    self.obj = Arbit.dialg_propts2(role, 'obj')
                    role.obj = self.obj
                elif obj_f == 3:
                    self.obj = Arbit.order_next(role, 'obj', self.target)
                    role.obj = self.obj
            except TrpgError as e:
                print('MESSAGE: ', e.value)
                role.obj = self.obj
        else:
            self.obj = objthing_m
            role.obj = self.obj

        # print('Route:',role.routes['S'].name,', sbj:',self.sbjthing_m.name,', obj:',self.objthing_m.name)