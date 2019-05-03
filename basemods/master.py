from basemods import TrpgError

class Master:
    master = dict()
    pid = 0

    def __init__(self, name, *args):
        self.name = name
        self.cls = self.__class__

        if self.cls.pid == 0:
            self.cls.pid += 1
            self.cls('', *args)
        else:
            self.pid = self.cls.pid
            self.cls.pid += 1

        if self.name in self.cls.master.keys():
            raise TrpgError('すでに名前 -{0}- の {1} オブジェクトは存在します'.format(self.name, self.cls.__name__))
        
        self.cls.master[self.name] = self

    def validate(self):
        return True