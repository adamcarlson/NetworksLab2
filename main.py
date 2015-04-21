__author__ = 'Adam Carlson, Thomas Lippert'
# assumption: the user will always input a valid HTTP command.

import mySocket as sk

HOST = '52.11.118.159'
PORT = 80
ADDR = (HOST, PORT)
BYTELEN = 100000

class HTTPRequestHandler(sk.BaseRequestHandler):
    def setup(self):
        self.command = input("Enter an HTTP command: ")

    def handle(self):
        self.command = self.command + ' HTTP/1.1\r\n' + 'Host: ' + HOST + '\r\n' * 2
        self.send(self.command)
        print(self.recv())

    def send(self, sentence):
        self.ComSocket.socket.send(sentence.encode())

    def recv(self):
        return self.ComSocket.socket.recv(BYTELEN).decode()


class FTPRequestHandler(sk.BaseRequestHandler):
    pass



def httpTest():
    ourSocket = sk.ComSocket()
    ourSocket.connect(ADDR)

    HTTPRequestHandler(ourSocket)
    ourSocket.close()

def ftpTest():
    ourSocket = sk.ComSocket()
    ourSocket.connect(ADDR)

    FTPRequestHandler(ourSocket)

    ourSocket.close()


if __name__ == "__main__":
    httpTest()