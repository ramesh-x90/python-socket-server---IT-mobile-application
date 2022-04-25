import json
from socket import socket


class User:
    def __init__(self , _username , _email , _password , _profileimage , _role) :
        self._username = _username
        self._email = _email
        self._password = _password
        self._profileimage = _profileimage
        self._role = _role
        self.conn : socket = None

    def setPicUrl(self , url : str):
        self._profileimage = url


    def userToJson(self ):
        return {
            '_username': self._username,
            '_email' : self._email,
            '_password' : self._password,
            '_profileimage' : self._profileimage,
            '_role' : self._role,
        }

    
    def userToJsonforOtherUsers(self ):
        return {
            '_username': self._username,
            '_email' : self._email,
            '_profileimage' : self._profileimage,
            '_role' : self._role,
        }


    @classmethod
    def fromJson(cls , jdict : dict):
        return cls(**jdict)

    def setSocket(self,socket : socket):
        self.conn = socket

    
    def sendAll(self, dataDict : dict):
        strData = (json.dumps(dataDict)+'[<->END<->]').encode()
        self.conn.sendall(strData)
        print('SERVER: ' + strData.decode())




