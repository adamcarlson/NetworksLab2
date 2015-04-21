__author__ = 'Adam Carlson'

import socket
import threading
from time import sleep

class ComSocket:
    def __init__(self, SC_address, request_handler_class):
        self.SCAddress = SC_address
        self.RequestHandlerClass = request_handler_class
        self.T_isShutdown = threading.Event()
        self.__shutdownRequest = False

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.SCAddress)
            self.__isServer = False
            self.RequestHandlerClass(self.socket, self.SCAddress, self)
            self.socket.close()
        except:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(self.SCAddress)
            self.__isServer = True
            self.socket.listen(5)
            self.ServeForever()

    def IsServer(self):
        if self.__isServer:
            return 1
        return 0

    def ServeForever(self):
        self.T_isShutdown.clear()
        try:
            while not self.__shutdownRequest:
                self.HandleRequest()
        finally:
            self.__shutdownRequest = False
            self.T_isShutdown.set()

    def Shutdown(self):
        self.__shutdownRequest = True
        self.T_isShutdown.wait()

    def HandleRequest(self):
        try:
            request, ADDR = self.socket.accept()    #get_request()
        except:
            print("Error <HandleRequest>: socket.accept()")
            return
        try:
            self.ProcessRequest(request, ADDR)
        except:
            print("Error <HandleRequest>: ProcessRequest()")

    def ProcessRequest(self, request, SC_address):
        self.RequestHandlerClass(request, SC_address, self)
        request.close()

class BaseRequestHandler:
    def __init__(self, request, SC_address, CS):
        self.request = request
        self.ADDR = SC_address
        self.CS = CS
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
