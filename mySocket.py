__author__ = 'Adam Carlson, Thomas Lippert'

import socket as sk

class ComSocket(object):
    def __init__(self):
        self.socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

    def connect(self, address):
        self.ADDR = address
        self.socket.connect(address)
        self.socket.settimeout(1)

    def close(self):
        self.socket.close()


class BaseRequestHandler:
    def __init__(self, ComSocket):
        self.ComSocket = ComSocket
        self.setup()
        self.handle()
        try:
            pass
        except:
            print("Error <BaseRequestHandler>: handle()")
        finally:
            self.finish()

    def send(self, sentence, encoding='utf-8'):
        self.ComSocket.socket.send(sentence.encode(encoding=encoding))

    def send_and_receive(self, sentence, encoding='utf-8'):
        self.send(sentence, encoding=encoding)
        while True:
            try:
                print(self.ComSocket.socket.recv(1024).decode(encoding='ascii'))
            except sk.timeout:
                return

    def recv(self, byteLen, encoding='utf-8'):
        return self.ComSocket.socket.recv(byteLen).decode(encoding=encoding)

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass