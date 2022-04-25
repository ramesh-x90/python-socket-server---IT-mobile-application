
import os
from pubSubServices import Service
from DataBase.CloudStor import CloudStore
import sys
from DataBase.Db import Db
import time
import socket
import threading
import ProtocolV1 as CurrentProtocol



def send_text(s: str):
    conn.send(s.encode())


def client_connection(conn: socket.socket):
    binaryBuffer = []
    connected = 1
    buffer = 1024*5
    cache = {
        'UserObj': None,
        'fileBinaryBuffer': binaryBuffer,

    }
    # nothing to do here
    # encord dytes to String
    # when passing images or documnets have to change this code

    AsingleReqbinary = None

    rowBytes = bytearray()

    while connected == 1:
        st = ""
        try:
            try:
                while True:

                    byteBuffer = conn.recv(buffer)

                    if len(byteBuffer) == 0:
                        connected = 0
                        break

                    rowBytes += byteBuffer

                    if byteBuffer.find(b'[<->END<->]') > -1:
                        break

            except Exception as e:
                print('Client left')
                break

            if connected == 0:
                break
     # nothing to do here for now

            # protocol update
            # check binnary data in recevied data (pdf , imgs)

            rowBytes = rowBytes[:rowBytes.find(b'[<->END<->]')]

            if rowBytes.find(b'\\"[<->BINARYDATA<->:]\\"') > -1:
                print('clietn is trying to do something sus')
                break

            flagIndex = rowBytes.find(b'[<->BINARYDATA<->:]', 0,)

            if flagIndex != -1:
                print('incomming binary data')
                print(len(rowBytes))
                # remover json String
                st = rowBytes[:flagIndex].decode()

                fileBinary = rowBytes[flagIndex:].replace(
                    b'[<->BINARYDATA<->:]', b'')

                # save this dinanry data on users buffer
                # we can access this buffer according to user req json strings
                binaryBuffer.append(fileBinary)

                # f = open('image.jpg' , "wb")
                # f.write(fileBinary)
                # f.close()

            else:
                st = rowBytes.decode()

            rowBytes.clear()
            # for testing
            print(st)

            # check protocol version
            # block if outdated

            if st == "protocol version=0.1.1":
                continue

            CurrentProtocol.hook(st, dataSources, conn, cache)

            # goto protocol version

            #reqest == register
            # decode register request save hash
            # send result

            # reqest == logging
            # remove token (expire token)
            # decode logging request
            # varification send
            #   send token (client will use this for next logging)

            # msg pass request
            # send msg to destinations
            # store msgs for offline users
            # if new forum thread create new forum thread
            ##

            ##
            ##  request == event_data
            # send event data (search from data base)
            ##

            # if == group adimn
            # post events_

            # add members
            # remove members

        except Exception as e:
            print('client Disconnected' + e)

            pass

    # remove client from online clients list
    conn.close()
    try:
        users.remove(cache['UserObj'])
    except Exception as e:
        pass
    
    threading.Thread(target=(Service.clientLeft), args=( )).start()
    print('client left')
    print(len(users))

import time
# HOST = '192.168.1.15'
HOST = '0.0.0.0'
PORT = 65400

print("[+] connecting mongodb" + 10*" ",end='')
data_base = Db()
time.sleep(0.2)
print("\r[+] mongodb connected"+ 10*" ",end='')


users=[] # active users




dataSources = {

    'mongoDb': data_base,
    'fireBase': CloudStore(),
    'users': users,
}



time.sleep(0.2)
print("\r[+] cloud store ready"+ 10*" ",end='')

global conn

print("\r[+] Creating server socket"+ 10*" ",end='')
sock = socket.socket()

try:
    sock.bind((HOST, PORT))
except Exception as e:
    print("ERROR := " + str(e))
    exit()
time.sleep(0.2)
print("\r[+] server socket binding successed"+ 10*" ",end='')

sock.listen()
print(f"\r[+] listing to port: {PORT}"+ 10*" ")




print('Starting Services')
Service.init(users)
print('Services Running')


while True:
    conn, address = sock.accept()
    
    print("[+] Address: " + str(address[0]) + " port : " + str(address[1]))

    t2 = threading.Thread(target=(client_connection), args=(conn, ))
    t2.start()
