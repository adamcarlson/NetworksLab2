__author__ = 'Adam Carlson'


import ComSocket, re

def main(NAME = "Adam Carlson"):

    HOST = 'localhost'
    PORT = 21567
    ADDR = (HOST, PORT)

    class RequestHandler(ComSocket.BaseRequestHandler):
        def setup(self):
            print("...Connection received from: {}".format(self.ADDR))
            self.request.send("You have Connected to {}".format(NAME).encode())
            if self.CS.IsServer():
                print(self.Recv(1024))


        def handle(self):
            while True:
                data = self.Recv(1024)
                if self.IsExit(data):
                    break
                print(data)
                data = input(">")
                self.Send(data)
                if self.IsExit(data):
                    break

        def finish(self):
            self.CS.Shutdown()

        def Send(self, data):
            self.request.send("{}: {}".format(NAME, data).strip().encode())

        def Recv(self, bitLen):
            return self.request.recv(bitLen).strip().decode()

        def IsExit(self, data):
            if re.match("\: [Ee][Xx][Ii][Tt]$", data):
                return 1
            return 0

    conSock = ComSocket.ComSocket(ADDR, RequestHandler)
    conSock.ServeForever()

if __name__ == "__main__":
    x = input("Enter Name: ")
    main(x)