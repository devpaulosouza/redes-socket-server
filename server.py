#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################
# File name: server.py                            #
###################################################
# author: Lauro Milagres Oliveira                 #
# author: Paulo Souza                             #
###################################################

import socket

HOST = '127.0.0.1'
PORT = 8484
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print('aguardando conexão...')

while True:
    conn, addr = s.accept()
    print ('consagrado no ip ' + addr[0] + ' se conectou.' )

    close = False

    while not close:
        try:
            data = conn.recv(1024)
        except socket.error:
            print ('Deu ruim...')
        if data:
            print (data.decode('utf-8'))
            conn.send('data'.encode())
            close = True