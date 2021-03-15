import logging

# --== BASE Settings ==--

# Уровень логирования по-умолчанию
LOGGING_LEVEL = logging.INFO
# Порт по умолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024

# --== Server Default settings ==--
# Максимальная очередь подключений
MAX_CONNECTIONS = 5

# --== Client default settings ==--


# --== Codes&Others ==--
# Кодировка проекта
ENCODING = 'utf-8'

# Прококол JIM основные ключи:
PROTOCOL_JIM_KEYS_DICT = {
    'ACTION': 'action',
    'TIME': 'time',
    'USER': 'user',
    'ACCOUNT_NAME': 'account_name',
    'MESSAGE_TEXT': 'message_text'
}

# Прочие ключи, используемые в протоколе
PROTOCOL_OTHER_KEYS_DICT = {
    'PRESENCE': 'presence',
    'RESPONSE': 'response',
    'ERROR': 'error',
    'MESSAGE': 'message'
}

SRV_MSG_DICT = {
    'BASE_INFORMATION': [100, 'базовое уведомление'],
    'IMPORTANT_INFORMATION': [101, 'важное уведомление'],
    'OK': [200, 'ок'],
    'CREATED': [201, 'объект создан'],
    'ACCEPTED': [202, 'подтверждение'],
    'ERROR_400': [400, 'неправильный запрос/JSON-объект'],
    'NOT_AUTHORIZED': [401, 'не авторизован'],
    'LOGIN_PASS_WRONG': [402, 'неправильный логин/пароль'],
    'FORBIDDEN': [403, 'пользователь заблокирован'],
    'NOT_FOUND': [404, 'пользователь/чат отсутствует на сервере'],
    'CONFLICT': [409, 'уже имеется подключение с указанным логином'],
    'OFFLINE': [410, 'адресат существует, но недоступен (offline)'],
    'SERVER_ERROR': [500, 'ошибка сервера'],
}
