import sys
import subprocess
from common.settings import ENCODING

from logs.cfg import client_log_config, server_log_config
# from common.my_classes import Launcher


# # да это не безопасно и коряво, но пока экономим время - причешем потом
# keys = dict(zip(sys.argv[1::2], sys.argv[2::2]))
# www = Launcher(**keys)


PROCESS = []

while True:
    print(f'Запущенные процессы: {PROCESS}')
    my_params = []
    if len(sys.argv) > 1:
        my_params = sys.argv[1:]
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер, '
                   'c - запустить клиентов, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen(['python3', 'server.py'] + my_params,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True))
    elif ACTION == 'c':
        for i in range(5):
            my_params2 = ['gnome-terminal', '--wait', '--', 'python3', 'client.py'] + my_params
            my_params2.append('mode')
            my_params2.append('listen' if (i != 3) else 'send')
            # print(my_params2)
            _ = subprocess.Popen(my_params2,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)

            # out, err = _.communicate()
            # if out:
            #     print('OUT:', out.decode(encoding=ENCODING))
            # if err:
            #     print('ERR:', err.decode(encoding=ENCODING))
            PROCESS.append(_)
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.send_signal(15)
            VICTIM.kill()



            # VICTIM.send_signal(2)
            # print(VICTIM.returncode)
            # VICTIM.kill()
