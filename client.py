import json
import sys
import logging
import logs.cfg.client_log_config

from common.my_classes import Client

CLIENT_LOGGER = logging.getLogger('client')

CLIENT_LOGGER.info(f'Запущен новый клиент')
CLIENT_LOGGER.debug(f'Переданы параметры командной строки {sys.argv}')
# да это не безопасно и коряво, но пока экономим время - причешем потом
keys = dict(zip(sys.argv[1::2], sys.argv[2::2]))
CLIENT_LOGGER.debug(f'Сформированы ключи {keys}')
CLIENT_LOGGER.debug(f'Попытка создать экземпляр клиента')
www = Client(**keys)
www.start()
# CLIENT_LOGGER.info(f'Создан экземпляр Клиента с указанными ключами')
# CLIENT_LOGGER.debug(f'Попытка подключиться к серверу')
# if www.connect():
#     CLIENT_LOGGER.info(f'Осуществлено соединение с сервером')
#     CLIENT_LOGGER.debug(f'Попытка создать "присутствие"')
#     message_to_server = www.create_presence()
#     CLIENT_LOGGER.debug(f'Создано приветственное сообщение{message_to_server}')
#     CLIENT_LOGGER.debug(f'Попытка послать сообщение')
#     www.send_message(www.my_socket, message_to_server)
#     CLIENT_LOGGER.debug(f'Сообщение послано')
#     try:
#         CLIENT_LOGGER.debug(f'Попытка получить и декодировать ответ')
#         answer = www.process_ans(www.get_message(www.my_socket))
#         CLIENT_LOGGER.debug(f'Получен ответ {answer}')
#         # print(answer)
#     except (ValueError, json.JSONDecodeError):
#         CLIENT_LOGGER.error(f'Не удалось декодировать сообщение сервера.')
#         # print('Не удалось декодировать сообщение сервера.')
# else:
#     CLIENT_LOGGER.critical(f'Ошибка подключения')