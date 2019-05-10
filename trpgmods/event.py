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
    
    def do(self, n):
        # インポート部分
        from basemods import Holder

        return Holder.master('Process', self.procs).deed(self.sbj, self.obj, n)
    
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

    def focus_out_first(self, role_first):
        # インポート部分
        from game import Game

        self.role_first = role_first
        return Game.dummy()

    def focus_in_first(self, *dummy):
        # インポート部分
        from game import Game

        if self.text != '':
            print(self.text)
        
        #文字送りで入力なし
        cap_f = self.cap_f()
        if cap_f == 1:
            return {'curr_func': Game.newline, 'arg': (), 'next_func': self.focus_newline}
        else:
            return {'curr_func': self.focus_out_sbj_role, 'arg': (), 'next_func': self.focus_in_sbj_role}

    def focus_newline(self, *dummy):
        return {'curr_func': self.role_first.way_out, 'arg': (), 'next_func': self.role_first.way_in}

    def focus_out_sbj_role(self):
        # インポート部分
        from basemods import Holder
        from game import Game

        role_f = self.role_f()
        sbjrole_m_str = self.sbjrole_m_str()

        rtn = Game.dummy()

        # 能動ロールの設定
        if sbjrole_m_str == '':
            if role_f in (1, 3):
                rtn = (Holder.master('Role').values(), 'Arbit', 'Role', 0)
            else:
                self.sbjrole = self.role_first
        else:
            self.sbjrole = Holder.master('Role', sbjrole_m_str)
        
        return rtn

    def focus_in_sbj_role(self, *dummy):
        return {'curr_func': self.focus_out_sbj_thing, 'arg': (), 'next_func': self.focus_in_sbj_thing}

    def focus_out_sbj_thing(self):
        # インポート部分
        from game import Game
        
        sbj_f = self.sbj_f()
        sbjthing_m = self.sbjthing_m()

        rtn = Game.dummy()

        # 能動者の設定
        if sbjthing_m.name == '':
            if sbj_f in (1, 2):
                rtn = (self.sbjrole.getpropts(), self.sbjrole.name, 'sbj', 0)
        
        return rtn

    def focus_in_sbj_thing(self, sbj):
        sbj_f = self.sbj_f()
        sbjthing_m = self.sbjthing_m()

        rtn = {'curr_func': self.focus_out_obj_role, 'arg': (), 'next_func': self.focus_in_obj_role}

        if sbjthing_m.name == '':
            if self.sbjrole.sbj.name == '':
                self.sbj = self.sbjrole.getpropts()[0]
            else:
                self.sbj = self.sbjrole.sbj
            # print('Role -{0}- のデフォルト能動者 -{1}-'.format(role.name, self.sbj.name))

            if sbj is not None:
                if sbj_f == 1:
                    self.sbj = sbj
                    self.sbjrole.sbj = sbj
                elif sbj_f == 2:
                    rtn = {'curr_func': self.focus_out_sbj_thing2, 'arg': (sbj,), 'next_func': self.focus_in_sbj_thing2}
                elif sbj_f == 3:
                    if self.target.name not in self.sbjrole.ordered['sbj'].keys():
                        self.sbjrole.ordered['sbj'][self.target.name] = self.sbjrole.order(self.target)

                    try:
                        self.sbj = next(self.sbjrole.ordered['sbj'][self.target.name])
                    except StopIteration:
                        self.sbjrole.ordered['sbj'][self.target.name] = self.sbjrole.order(self.target)
                        self.sbj = next(self.sbjrole.ordered['sbj'][self.target.name])
                        
                    self.sbjrole.sbj = self.sbj
        else:
            self.sbj = sbjthing_m
            self.sbjrole.sbj = self.sbj
        
        return rtn

    def focus_out_sbj_thing2(self, sbj):        
        return (sbj.getpropts(), sbj.name, 'sbj', 0)

    def focus_in_sbj_thing2(self, sbj):
        if sbj is not None:
            self.sbj = sbj
        return {'curr_func': self.focus_out_obj_role, 'arg': (), 'next_func': self.focus_in_obj_role}

    def focus_out_obj_role(self):
        # インポート部分
        from basemods import Holder
        from game import Game

        role_f = self.role_f()
        objrole_m_str = self.objrole_m_str()

        rtn = Game.dummy()

        # 受動ロールの設定
        if objrole_m_str == '':
            if role_f in (2, 3):
                rtn = (Holder.master('Role').values(), 'Arbit', 'Role', 0)
            else:
                self.objrole = self.role_first
        else:
            self.objrole = Holder.master('Role', objrole_m_str)
        
        return rtn

    def focus_in_obj_role(self, *dummy):
        return {'curr_func': self.focus_out_obj_thing, 'arg': (), 'next_func': self.focus_in_obj_thing}

    def focus_out_obj_thing(self):
        # インポート部分
        from game import Game
        
        obj_f = self.obj_f()
        objthing_m = self.objthing_m()

        rtn = Game.dummy()

        # 能動者の設定
        if objthing_m.name == '':
            if obj_f in (1, 2):
                rtn = (self.objrole.getpropts(), self.objrole.name, 'obj', 0)
        
        return rtn

    def focus_in_obj_thing(self, obj):
        obj_f = self.obj_f()
        objthing_m = self.objthing_m()

        rtn = {'curr_func': self.role_first.way_out, 'arg': (), 'next_func': self.role_first.way_in}

        if objthing_m.name == '':
            if self.objrole.obj.name == '':
                self.obj = self.objrole.getpropts()[0]
            else:
                self.obj = self.objrole.obj
            # print('Role -{0}- のデフォルト能動者 -{1}-'.format(role.name, self.obj.name))

            if obj is not None:
                if obj_f == 1:
                    self.obj = obj
                    self.objrole.obj = obj
                elif obj_f == 2:
                    rtn = {'curr_func': self.focus_out_obj_thing2, 'arg': (obj,), 'next_func': self.focus_in_obj_thing2}
                elif obj_f == 3:
                    if self.target.name not in self.objrole.ordered['obj'].keys():
                        self.objrole.ordered['obj'][self.target.name] = self.objrole.order(self.target)

                    try:
                        self.obj = next(self.objrole.ordered['obj'][self.target.name])
                    except StopIteration:
                        self.objrole.ordered['obj'][self.target.name] = self.objrole.order(self.target)
                        self.obj = next(self.objrole.ordered['obj'][self.target.name])
                        
                    self.objrole.obj = self.obj
        else:
            self.obj = objthing_m
            self.objrole.obj = self.obj
        
        return rtn

        # print('Route:',self.role_first.routes['S'].name,', sbj:',self.sbjthing_m.name,', obj:',self.objthing_m.name)

    def focus_out_obj_thing2(self, obj):        
        return (obj.getpropts(), obj.name, 'obj', 0)

    def focus_in_obj_thing2(self, obj):
        if obj is not None:
            self.obj = obj
        return {'curr_func': self.role_first.way_out, 'arg': (), 'next_func': self.role_first.way_in}