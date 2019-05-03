from iotemp import Scenario
# from trpgmods import Role

class Game:
    def __init__(self, roles):

        # インポート部分
        from trpgmods import Role

        # [Role()]
        self.roles = [Role.master[v] for v in roles]
    
    def validate(self):
        # インポート部分
        from basemods import Holder

        Holder.buildvalid()
        self.roles[0].routes.append(Scenario().wizard)
    
    def start(self):
        self.validate()

        endflg = True
        while endflg:
            for i in self.roles:
                i.action()
