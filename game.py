from basemods import TrpgError, Master, Arbit
# from trpgmods import Role

class Game:
    def __init__(self, roles):

        # インポート部分
        from basemods import Holder
        from trpgmods import Role

        Holder.buildvalid()
        Game.roles = [Role.master[v] for v in roles] # [Role()]
        Game.roles[0].wizard_f = True
    
    @classmethod
    def newline(self):
        class A:
            name = 'Enter'
        return ([A], '', '', False)
    
    @classmethod
    def dummy(self):
        return (list(), '', '', False)

    @classmethod
    def argdic_first(self, *dummy):
        return {'curr_func': Game.start_out, 'arg': (Game.roles, 'None', 'role', 0), 'next_func': Game.start_in}
    
    @classmethod
    def start_out(self, *arg):
        return arg
    
    @classmethod
    def start_in(self, role):
        if role is None:
            role = Game.roles[0]
        return {'curr_func': role.action_out, 'arg': (), 'next_func': role.action_in}