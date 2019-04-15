from inspect import signature

class ClassTemp:
    def __init__(self, classt):
        self.sig = signature(classt.__init__).parameters

        for i in list(self.sig)[1:]:
            print(self.sig[i])

