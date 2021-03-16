import json
import sys
import select
import socket
import time
import logging
import inspect

from common.metaclasses import MetaVerifier

from common.settings import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_PACKAGE_LENGTH, \
    ENCODING, MAX_CONNECTIONS, PROTOCOL_JIM_KEYS_DICT, PROTOCOL_OTHER_KEYS_DICT, SRV_MSG_DICT

import logs.cfg.server_log_config
import logs.cfg.client_log_config


def log(f):
    def wrapper(*args, **kwargs):
        # print(args[0].__class__.__name__.lower())
        # LOGGER = logging.getLogger(inspect.currentframe().f_back.f_locals['__class__'].__name__.lower())
        LOGGER = logging.getLogger(args[0].__class__.__name__.lower())
        LOGGER.debug(
            f'Вызвана функция {f.__name__} из модуля {f.__module__} c параметрами args: {args[1:]}, kwargs: {kwargs}')
        return f(*args, **kwargs)

    return wrapper


class BaseClass(metaclass=MetaVerifier):
    objects_count = 0
    LOGGER = logging.getLogger('server')

    @log
    def __init__(self, *args, **kwargs):
        self.ip_adr = DEFAULT_IP_ADDRESS if not kwargs.get('ip_adr') else kwargs.get('ip_adr')
        self.port = int(DEFAULT_PORT if not kwargs.get('port') else kwargs.get('port'))
        self.max_package_len = int(MAX_PACKAGE_LENGTH if not kwargs.get('max_package_len')
                                   else kwargs.get('max_package_len'))
        self.my_socket = None
        self.login = 'Guest' if not kwargs.get('login') else kwargs.get('name')
        self.__class__.objects_count += 1

    # @log
    def __del__(self):
        # self.__class__.LOGGER.debug(f'Удаление экземпляра {self}')
        self.__class__.objects_count -= 1

    @log
    def __setattr__(self, key, value):
        self.__class__.LOGGER.debug(f'Атрибут "{key}" установлен в "{value}"')
        super().__setattr__(key, value)

    @log
    def get_message(self, client, enc=ENCODING):
        try:
            encoded_response = client.recv(self.max_package_len)
            if isinstance(encoded_response, bytes):
                json_response = encoded_response.decode(enc)
                response = json.loads(json_response)
                if isinstance(response, dict):
                    return response
                raise ValueError
            raise ValueError
        except Exception as err:
            self.__class__.LOGGER.error(f'Ошибка получения сообщения от "{client}":"{err}"')

    @log
    def send_message(self, client, response, enc=ENCODING):
        try:
            js_message = json.dumps(response)
            encoded_message = js_message.encode(enc)
            client.send(encoded_message)
        except Exception as err:
            self.__class__.LOGGER.error(f'Ошибка отправки сообщения "{response}" клиенту "{client}":"{err}"')


class Client(BaseClass):

    @log
    def __init__(self, *args, **kwargs):
        self.__class__.LOGGER = logging.getLogger('client')
        super().__init__(*args, **kwargs)
        self.client_mode = 'listen' if kwargs.get('mode') not in ['listen', 'send'] else kwargs.get('mode')
        self.__class__.LOGGER.debug(f'Создан экземпляр {self.__class__.__name__}:{self}')
        self._message = ''

    @log
    def connect(self):
        self.__class__.LOGGER.debug('Создание сокета')
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__class__.LOGGER.debug('Открытие коннекта')
        try:
            self.my_socket.connect((self.ip_adr, self.port))
            return True
        except Exception as err:
            self.__class__.LOGGER.error(f'Ошибка коннекта:{err}')
            return False

    @log
    def disconnect(self):
        self.__class__.LOGGER.debug('Закрытие сокета')
        self.my_socket.close()

    @log
    def exit(self):
        self.__class__.LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)

    @log
    def create_message(self, message_text=None, message_type='MESSAGE'):
        self.__class__.LOGGER.debug(f'Попытка создать сообщение...')
        _ = {
            PROTOCOL_JIM_KEYS_DICT['ACTION']: PROTOCOL_OTHER_KEYS_DICT[message_type],
            PROTOCOL_JIM_KEYS_DICT['TIME']: time.time(),
            PROTOCOL_JIM_KEYS_DICT['USER']: self.login,
            PROTOCOL_JIM_KEYS_DICT['MESSAGE_TEXT']: message_text if message_text else self._message
        }
        self.__class__.LOGGER.debug(f'Создано сообщение типа {message_type}: {_}')
        return _

    @log
    def decode_message(self, message=None):
        pass

    @log
    def start(self):
        self.__class__.LOGGER.debug(f'Попытка подключиться к серверу')
        if self.connect():
            while True:
                if self.client_mode == 'send':
                    self.__class__.LOGGER.debug(f'Клиент запущен в качестве Сендера')
                    self._message = input('Введите сообщение для отправки или \'!!!\' для завершения работы: ')
                    if self._message == '!!!':
                        self.disconnect()
                        self.exit()
                    self.send_message(self.my_socket, self.create_message())
                elif self.client_mode == 'listen':
                    self.__class__.LOGGER.debug(f'Клиент запущен в качестве слушателя')
                    self._message = self.get_message(self.my_socket)
                    self.__class__.LOGGER.info(f'Получено сообщение {self._message}')
                    print(f'Получено сообщение от пользователя '
                          f'{self._message[PROTOCOL_JIM_KEYS_DICT["USER"]]}:'
                          f'\n{self._message[PROTOCOL_JIM_KEYS_DICT["MESSAGE_TEXT"]]}')
        else:
            self.__class__.LOGGER.critical(f'Ошибка подключения')

    # Переписать нафиг
    @log
    def create_presence(self, account_name='Guest'):
        _ = {
            PROTOCOL_JIM_KEYS_DICT['ACTION']: PROTOCOL_OTHER_KEYS_DICT['PRESENCE'],
            PROTOCOL_JIM_KEYS_DICT['TIME']: time.time(),
            PROTOCOL_JIM_KEYS_DICT['USER']: {
                PROTOCOL_JIM_KEYS_DICT['ACCOUNT_NAME']: account_name
            }
        }
        self.__class__.LOGGER.debug(f'Создание приветствия {_}')
        return _

    # Переписать этот бред
    @log
    def process_ans(self, message):
        if PROTOCOL_OTHER_KEYS_DICT['RESPONSE'] in message:
            if message[PROTOCOL_OTHER_KEYS_DICT['RESPONSE']] == 200:
                self.__class__.LOGGER.debug(f'Получен ответ:{SRV_MSG_DICT["OK"]}')
                return f'{SRV_MSG_DICT["OK"]}'
            self.__class__.LOGGER.debug(f'Получен ответ:{SRV_MSG_DICT["ERROR_400"]}')
            return f'{SRV_MSG_DICT["ERROR_400"]} : {message[PROTOCOL_OTHER_KEYS_DICT["ERROR"]]}'
        self.__class__.LOGGER.error('Непонятный ответ')
        raise ValueError


class Server(BaseClass):

    @log
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_connections = MAX_CONNECTIONS if not kwargs.get('max_connections') else kwargs.get('max_connections')
        self.clients = []
        self.recv_data_lst = []
        self.send_data_lst = []
        self.err_lst = []
        self.message_lst = []

    @log
    def bind(self):
        self.__class__.LOGGER.debug('Создание сокета')
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__class__.LOGGER.debug('Бинд сервера')
        try:
            self.my_socket.bind((self.ip_adr, self.port))
        except Exception as err:
            self.__class__.LOGGER.critical(f'ОШИБКА!: {err}')
            return False
        return True

    @log
    def start_server(self):
        self.my_socket.listen(self.max_connections)
        while True:
            client, client_address = self.my_socket.accept()
            try:
                message_from_client = self.get_message(client)
                self.__class__.LOGGER.info(f'Сообщение от клиента: {message_from_client}')
                # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
                response = self.process_client_message(message_from_client)
                self.send_message(client, response)
                client.close()
            except (ValueError, json.JSONDecodeError):
                self.__class__.LOGGER.error('Принято некорретное сообщение от клиента.')
                self.__class__.LOGGER.debug('Закрытие соединения')
                client.close()

    @log
    def start_server2(self):
        self.my_socket.settimeout(0.5)
        self.my_socket.listen(self.max_connections)
        while True:
            # self.__class__.LOGGER.info(f'Слушаю...')
            self.send_data_lst = []
            self.recv_data_lst = []
            self.err_lst = []
            try:
                client, client_address = self.my_socket.accept()
            except OSError:
                pass
            else:
                self.__class__.LOGGER.info(f'Установлено соедение с ПК {client_address}')
                self.__class__.LOGGER.info(f'В список клиентов {self.clients} добавляем {client}')
                self.clients.append(client)
            try:
                if self.clients:
                    self.recv_data_lst, self.send_data_lst, self.err_lst = select.select(self.clients,
                                                                                         self.clients, [], 0)
            except OSError:
                pass

            if len(self.recv_data_lst) > 0:
                self.get_messages()
            if len(self.message_lst) > 0 and len(self.send_data_lst) > 0:
                self.send_messages()

    @log
    def get_messages(self):
        for _ in self.recv_data_lst:
            self.__class__.LOGGER.debug(f'Попытка получить сообщение от {_}')
            answer = self.get_message(_)
            self.__class__.LOGGER.debug(f'Ответ {answer}')
            if answer:
                self.__class__.LOGGER.info(f'В список сообщений {self.message_lst} добавляем {answer}')
                self.message_lst.append(answer)
            else:
                # pass
                self.__class__.LOGGER.info(f'Из списка клиентов {self.clients} удаляем {_}')
                self.clients.remove(_)

    @log
    def send_messages(self):
        for message in self.message_lst:
            for _ in self.send_data_lst:
                self.send_message(_, message)
            self.__class__.LOGGER.info(f'Из списка сообщений {self.message_lst} удаляем {message}')
            self.message_lst.remove(message)

    @log
    def process_client_message(self, message):
        if PROTOCOL_JIM_KEYS_DICT['ACTION'] in message \
                and message[PROTOCOL_JIM_KEYS_DICT['ACTION']] == PROTOCOL_OTHER_KEYS_DICT['PRESENCE'] \
                and PROTOCOL_JIM_KEYS_DICT['TIME'] in message \
                and PROTOCOL_JIM_KEYS_DICT['USER'] in message \
                and message[PROTOCOL_JIM_KEYS_DICT['USER']][PROTOCOL_JIM_KEYS_DICT['ACCOUNT_NAME']] == 'Guest':
            self.__class__.LOGGER.debug(f'Передаю ответ: {PROTOCOL_OTHER_KEYS_DICT["RESPONSE"]}:{200}')
            return {PROTOCOL_OTHER_KEYS_DICT['RESPONSE']: 200}
        self.__class__.LOGGER.error(f'Передаю ответ: {PROTOCOL_OTHER_KEYS_DICT["RESPONSE"]}:{400}')
        return {
            PROTOCOL_OTHER_KEYS_DICT['RESPONSE']: 400,
            PROTOCOL_OTHER_KEYS_DICT['ERROR']: 'Bad Request'
        }


if __name__ == '__main__':
    www = Server({'ip_adr': '127.0.0.1'})
    eee = ClientSender({'ip_adr': '127.0.0.5'})

"""
class Launcher:
    def __init__(self, *args, **kwargs):
        self.argv_dict = kwargs
        self.servers_list = []
        self.clients_list = []

    def create_server(self):
        self.servers_list.append(Server(self.argv_dict))

    def create_client(self):
        self.clients_list.append(Client(self.argv_dict))
"""

"""
class Log:
    LOGGER = logging.getLogger('server')

    def __call__(self, func_to_log):
        def log_me(*args, **kwargs):
            Log.LOGGER.info(f'Вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}')
            my_return = func_to_log(*args, **kwargs)
            Log.LOGGER.info(f'Вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}')
            return my_return
        return log_me(self)
"""
