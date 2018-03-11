#!/usr/bin/env python3
# server.py
# author: Bernard Tourneur & Jonathan Miel
# version: March 6, 2018

import socket
import sys
from chat import Chat
import json

SERVER_ADDRESS = (socket.gethostname(), 6000) 
print (SERVER_ADDRESS)

class server :
    def __init__ (self): 
        self.__sckt = socket.socket () #TCP coms client-server
        self.__sckt.bind (SERVER_ADDRESS)
        self.__clients = {}

    def run (self):
        self.__sckt.listen ()
        while True:
            client, addr = self.__sckt.accept () #client is a new socket, addr is a IPV4 address
            print (client.gethostname ())
            self.__clients [client.gethostname ()] = addr #clients name are the keys
            self._sendClients ()

    def _sendClients (self, client):
        infos = (json.dumps(self.__clients, indent= 4)).encode ()
        totalsent = 0
        try:
            while totalsent < len (infos):
                sent = client.send (infos[totalsent:])
                totalsent +=sent 
        except OSError:
            print ('Error while sending the message.')
        return self.__clients

class client :
    def __init__ (self):
        self.__cSckt = socket.socket () #TCP coms client-server

    def run (self):
        try :
            self.__cSckt.connect (SERVER_ADDRESS)
            self._getClients ()
        except OSError:
            print ('Server unfound, connexion failed.')
        
    def _getClients (self):
        parts = []
        done = False
        while not done :
            data = self.__cSckt.recv (1024)
            parts.append (data)
            done = data == b''
        infos = (b''.join (parts)).decode ()
        print (infos)
        return infos

if __name__ == '__main__':
    if len (sys.argv) == 2 and sys.argv [1] == 'server':
        server().run ()
    elif len (sys.argv) == 2 and sys.argv [1]== 'client':
        client().run ()
    elif len(sys.argv) == 3:
        Chat(sys.argv[1], int(sys.argv[2])).run()
    elif (sys.argv) == 2 and sys.argv [1] == 'chat':
        Chat().run()