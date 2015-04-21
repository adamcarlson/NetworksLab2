__author__ = 'Adam Carlson, Thomas Lippert'
# assumption: the user will always input a valid HTTP command.

import mySocket as sk
import socket
import re

HOST = '52.11.118.159'
HTTPPORT = 80
FTPPORT = 21
DATAPORT = 10001

class HTTPRequestHandler(sk.BaseRequestHandler):
    def setup(self):
        self.command = input("Enter an HTTP command: ")

    def handle(self):
        self.command = self.command + ' HTTP/1.1\r\n' + 'Host: ' + HOST + '\r\n' * 2
        self.send(self.command)
        print(self.recv(100000))



class FTPRequestHandler(sk.BaseRequestHandler):
    def setup(self):
        self.print_response()
        self.send('USER adam' + '\r\n', encoding='ascii')
        self.recv(1024, encoding='ascii')
        self.send('PASS adamandtom!' + '\r\n', encoding='ascii')
        self.print_response()

    def handle(self):
        self.quit = False
        while not self.quit:
            cmd = input('> ')
            func = getattr(self, cmd[:4].strip().lower())
            if len(cmd) > 4:
                func(cmd[5:])
            else:
                func()


    def print_response(self):
        print(self.recv(1024, encoding='ascii'))

    def print_data_response(self):
        print(self.dataSocket.recv(1024).decode(encoding='ascii'))

    def push(self):
        pass

    def retr(self):
        pass

    def quit(self):
        self.quit = True
        self.send('QUIT\r\n', encoding='ascii')

    def list(self):
        self.pasv()
        self.send('LIST\r\n', encoding='ascii')
        self.print_data_response()

    def get_port(self):
        data = self.recv(1024, encoding='ascii')
        p1, p2 = data[:-3].split(',')[-2:]
        return int(p1) * 256 + int(p2)

    def pasv(self):
        self.send('PASV\r\n', encoding='ascii')
        self.dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dataSocket.connect((HOST, self.get_port()))

def httpTest():
    address = (HOST, HTTPPORT)
    ourSocket = sk.ComSocket()
    ourSocket.connect(address)

    HTTPRequestHandler(ourSocket)
    ourSocket.close()

def ftpTest():
    address = (HOST, FTPPORT)
    ourSocket = sk.ComSocket()
    ourSocket.connect(address)

    FTPRequestHandler(ourSocket)

    ourSocket.close()


if __name__ == "__main__":
    ftpTest()