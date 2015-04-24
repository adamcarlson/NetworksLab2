__author__ = 'Adam Carlson, Thomas Lippert'
# assumption: the user will always input a valid HTTP command.

import mySocket as sk
import socket
from time import sleep

HOST = '52.11.118.159'
HTTPPORT = 80
FTPPORT = 21

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
        self.quitSession = False
        while not self.quitSession:
            cmd = input('> ')
            func = getattr(self, cmd[:4].strip().lower())
            if len(cmd) > 4:
                func(cmd[5:].strip())
            else:
                func()

    def finish(self):
        self.ComSocket.close()

    def print_response(self):
        print(self.recv(1024, encoding='ascii'))

    def print_data_response(self):
        print(self.dataSocket.recv(1024).decode(encoding='ascii'))

    def stor(self, data):
        self.send_and_receive('TYPE I\r\n', encoding='ascii')
        self.pasv()
        self.send_and_receive('STOR {}\r\n'.format(data), encoding='ascii')
        self.send_file()
        self.dataSocket.close()
        self.print_response()

    def send_file(self):
        filename = input("Enter the name/path of the file to be sent: ")
        file = open(filename, 'rb')
        self.dataSocket.send(file.read().decode().encode(encoding='ascii'))

    def retr(self, data):
        self.send_and_receive('TYPE I\r\n', encoding='ascii')
        self.pasv()
        self.send('RETR {}\r\n'.format(data), encoding='ascii')
        self.print_response()
        self.save_and_print_file(data)
        self.dataSocket.close()

    def save_and_print_file(self, filename):
        if '/' in filename:
            filename = filename.split("/")[-1]
        file = open(filename, 'wb')
        data = self.dataSocket.recv(100000)
        print(data)
        if input("Would you like to edit this file? ").lower().strip()[0] is 'y':
            data = data.decode().replace('Hello world!', input('Enter new body, pls: '))
        file.write(data.encode())
        file.close()

    def pwd(self):
        self.send_and_receive('PWD\r\n', encoding='ascii')

    def dele(self, data):
        self.send_and_receive('DELE {}\r\n'.format(data), encoding='ascii')

    def quit(self):
        self.quitSession = True
        self.send('QUIT\r\n', encoding='ascii')
        self.print_response()

    def list(self):
        self.pasv()
        self.send_and_receive('LIST\r\n', encoding='ascii')
        self.print_data_response()
        self.dataSocket.close()

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
    httpTest()
    ftpTest()
    httpTest()