import sys
from pathlib import Path

import unittest

print(Path.cwd().parent)
sys.path.append(Path.cwd().parent)
sys.path.append(Path.cwd().parent.joinpath('common'))

from common.my_classes import Client, Server


class TestClient(unittest.TestCase):
    def setUp(self):
        # Выполнить настройку тестов (если необходимо)
        init_dict = {'ip_adr': '127.0.0.55',
                     'port': '7788',
                     'max_package_len': '100',
                     }
        self.obj_param = Client(**init_dict)
        self.obj = Client()

    def tearDown(self):
        # Выполнить завершающие действия (если необходимо)
        pass

    def test_client_ip_adr_kwargs(self):
        self.assertEqual(self.obj_param.ip_adr, '127.0.0.55')

    def test_client_port_kwargs(self):
        self.assertEqual(self.obj_param.port, 7788)

    def test_client_mpl_kwargs(self):
        self.assertEqual(self.obj_param.max_package_len, 100)

    def test_client_ip_adr(self):
        self.assertEqual(self.obj.ip_adr, '127.0.0.1')

    def test_client_port(self):
        self.assertEqual(self.obj.port, 7777)

    def test_client_mpl(self):
        self.assertEqual(self.obj.max_package_len, 1024)


class TestServer(unittest.TestCase):
    def setUp(self):
        # Выполнить настройку тестов (если необходимо)
        init_dict = {'ip_adr': '127.0.0.55',
                     'port': '7788',
                     'max_package_len': '100',
                     }
        self.obj_param = Server(**init_dict)
        self.obj = Server()

    def tearDown(self):
        # Выполнить завершающие действия (если необходимо)
        pass

    def test_server_ip_adr_kwargs(self):
        self.assertEqual(self.obj_param.ip_adr, '127.0.0.55')

    def test_server_port_kwargs(self):
        self.assertEqual(self.obj_param.port, 7788)

    def test_server_mpl_kwargs(self):
        self.assertEqual(self.obj_param.max_package_len, 100)

    def test_server_ip_adr(self):
        self.assertEqual(self.obj.ip_adr, '127.0.0.1')

    def test_server_port(self):
        self.assertEqual(self.obj.port, 7777)

    def test_server_mpl(self):
        self.assertEqual(self.obj.max_package_len, 1024)


if __name__ == '__main__':
    unittest.main()
