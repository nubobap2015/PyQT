from common.settings import DEFAULT_PORT


class ServerPort:
    def __init__(self):
        self._value = DEFAULT_PORT

    def __set__(self, instance, value):
        if int(value) < 0:
            raise ValueError('Порт дожен быть > 0')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name
