from socket import SocketType, socket
import threading
from Models.User import User

import json


class Service():
    onlineUsers = []

    @classmethod
    def init(cls,clients: list):
        cls.onlineUsers=clients
        pass

    @classmethod    
    def clientAdded(cls):
        cls.notifyClientCountToOtherClients()
        pass

    @classmethod
    def clientLeft(cls):
        cls.notifyClientCountToOtherClients()
        pass

    @classmethod
    def notifyClientCountToOtherClients(cls):
        data = {
                '_responseType':'onlineUsersCount',
                'Count':len(cls.onlineUsers)
                }
        cls.sendAll(data)
        pass

    @classmethod
    def sendAll(cls,data : dict):
        for client in cls.onlineUsers:
            print(f"service Controller:{data}")
            client.sendAll(data)  



