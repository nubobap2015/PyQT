import dis
from tabulate import tabulate

class MetaVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = set()
        attrs = set()

        if clsname == 'Client':
            for _ in clsdict:
                if str(type(clsdict[_])) == "<class 'function'>":
                    for __ in dis.get_instructions(clsdict[_]):
                        if __.opname == 'LOAD_GLOBAL':
                            methods.add(__.argval)
                        elif __.opname == 'LOAD_ATTR':
                            attrs.add(__.argval)
        elif clsname == 'Server':
            pass
        elif clsname == 'BaseClass':
            pass
        else:
            pass

        print(methods)
        # print(tabulate(methods, tablefmt="grid"))
        super().__init__(clsname, bases, clsdict)
