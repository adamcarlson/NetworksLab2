__author__ = 'Adam Carlson, Thomas Lippert'

import socket as sk

class ComSocket(object):
    def __init__(self):
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    def connect(self, address):
        self.ADDR = address
        self.socket.connect(address)

    def close(self):
        self.socket.close()


class BaseRequestHandler:
    def __init__(self, ComSocket):
        self.ComSocket = ComSocket
        self.setup()
        try:
            self.handle()
        except:
            print("Error <BaseRequestHandler>: handle()")
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass