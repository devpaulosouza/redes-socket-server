#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################################################
# File name: server.py                            #
###################################################
# author: Lauro Milagres Oliveira                 #
# author: Paulo Souza                             #
###################################################

import socket

class Jogo(Tabuleiro):
    def __init__(self):
        super().__init__(tabuleiro)
        self.id = 0


class Jogador:
    def __init__(self):
        self.id = 0
        self.nome = 0
        

class Tabuleiro:
    def __init__(self):
        self.tamanho_linhas = 10
        self.tamanho_colunas = 10
        self.tabuleiro = 0

    def Tabuleiro(self):
        tabuleiro = []
        for linha in self.tamanho_linhas:
            board = []
            for coluna in self.tamanho_colunas:
                board.append(linha)
            tabuleiro.append(board)
        return tabuleiro

# Endereco do servidor
HOST = ''
# Porta do servidor
PORT = input("Insira a porta: ")

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
