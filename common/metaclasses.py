import dis
from tabulate import tabulate


class MetaVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = set()
        attrs = set()

        for _ in clsdict:
            if str(type(clsdict[_])) == "<class 'function'>":
                for __ in dis.get_instructions(clsdict[_]):
                    if __.opname in ['LOAD_GLOBAL', 'LOAD_METHOD', 'LOAD_DEREF']:
                        methods.add(__.argval)
                    elif __.opname in ['LOAD_FAST', 'STORE_FAST', 'LOAD_ATTR']:
                        attrs.add(__.argval)
                    # print(clsname, dis.dis(clsdict[__]))
                for __ in dis.get_instructions(_):
                    if __.opname in ['LOAD_GLOBAL', 'LOAD_METHOD', 'LOAD_DEREF', 'LOAD_NAME']:
                        methods.add(__.argval)
                    elif __.opname in ['LOAD_FAST', 'STORE_FAST', 'LOAD_ATTR']:
                        attrs.add(__.argval)

        if clsname == 'Client':
            pass
        elif clsname == 'Server':
            pass
        elif clsname == 'BaseClass':
            pass
        else:
            pass

        # print('\n', clsname)
        # print(tabulate([attrs, methods], tablefmt="grid")) #, tablefmt="grid"
        super().__init__(clsname, bases, clsdict)
