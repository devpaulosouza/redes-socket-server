#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################################################
# File name: server.py                                                                               #
######################################################################################################
# author: Lauro Milagres Oliveira                                                                    #
# author: Paulo Souza                                                                                #
######################################################################################################

import socket


######################################################################################################
#                                               Class Jogo                                           #
######################################################################################################

class Jogo:
    
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2



######################################################################################################
#                                             Class Jogador                                          #
######################################################################################################

class Jogador(Tabuleiro):
    
    def __init__(self, id, nome):
        super().__init__(tabuleiro)
        self.id = id
        self.nome = nome


######################################################################################################
#                                            Class Tabuleiro                                         #
######################################################################################################

class Tabuleiro:

    def __init__(self):
        self.tamanho_linhas = 10
        self.tamanho_colunas = 10
        self.tabuleiro = self.Tabuleiro()

    def Tabuleiro(self):
        tabuleiro = []
        for linha in self.tamanho_linhas:
            board = []
            for coluna in self.tamanho_colunas:
                board.append(linha)
            tabuleiro.append(board)
        return tabuleiro

######################################################################################################
#                                       Class Converte para Json                                     #
######################################################################################################

class ConvertJson:
    pass



######################################################################################################

if __name__ == "__main__":
    
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
