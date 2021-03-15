import logging
import sys

import logs.cfg.server_log_config

SERVER_LOGGER = logging.getLogger('server')

from common.my_classes import Server

SERVER_LOGGER.info(f'Запущен новый сервер')
SERVER_LOGGER.debug(f'Переданы параметры командной строки {sys.argv}')

# да это не безопасно и коряво, но пока экономим время - причешем потом
keys = dict(zip(sys.argv[1::2], sys.argv[2::2]))
SERVER_LOGGER.debug(f'Сформированы ключи {keys}')
SERVER_LOGGER.debug(f'Попытка создать экземпляр Сервера')
www = Server(**keys)
SERVER_LOGGER.info(f'Экземпляр Сервера создан')
SERVER_LOGGER.debug(f'Биндим сервер')
if www.bind():
    SERVER_LOGGER.info(f'Запуск сервера')
    www.start_server2()
else:
    SERVER_LOGGER.critical(f'Запуск сервера провален!')
    del www
    exit()