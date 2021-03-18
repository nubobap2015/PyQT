
class ServerPort:
    def __init__(self):
        self._value = 7776

    def __set__(self, instance, value):
        print('__set__: ', value)
        if int(value) < 0:
            raise ValueError('Порт дожен быть > 0')
        self._value = value
