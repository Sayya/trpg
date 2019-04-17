from inspect import signature

class Template:
    def __init__(self, classt):
        self.sig = signature(classt.__init__).parameters

        for i in list(self.sig)[1:]:
            print('<name>={0} : <default>={1} : <class>={3}'.format(self.sig[i].name, self.sig[i].default, self.sig[i].default.__class__))
            chkstr = input()
            arglis[i] = chkstr

