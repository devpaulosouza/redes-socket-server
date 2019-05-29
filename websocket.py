#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################################################
# File name: server.py                                                                               #
######################################################################################################
# author: Lauro Milagres Oliveira                                                                    #
# author: Paulo Souza                                                                                #
######################################################################################################

# {'action': 'start', 'username': 'paulo'}
# salvar jogo e user para dois players, depois associar cada comando do jogo


import asyncio
import json
import logging
import websockets


######################################################################################################
#                                               Class Jogo                                           #
######################################################################################################
# Matriz possue posicoes zeradas, ou seja campo vazio,
# valor 10 para as posicoes dos navios
# valor 5 para as posicoes que foram acertadas
#
######################################################################################################

class Jogo:
    
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2


######################################################################################################
#                                             Class Jogador                                          #
######################################################################################################

class Jogador:
    
    def __init__(self, id, nome,board):
        Quadro.__init__(board)
        self.id = id
        self.nome = nome


######################################################################################################
#                                            Class Tabuleiro                                         #
######################################################################################################

class Quadro:

    def __init__(self,board):
        self.tamanho_linhas = 10
        self.tamanho_colunas = 10
        self.board = board
        self.tabuleiro = self.Tabuleiro()
        self.tabuleiroPosicionado = self.PosicaoDosNavios()

    # montando o tabuleiro 10x10 vazio
    def Tabuleiro(self):
        tabuleiro = []
        for linha in self.tamanho_linhas:
            board = []
            for coluna in self.tamanho_colunas:
                board.append(linha)
            tabuleiro.append(board)
        return tabuleiro
    
    def PosicaoDosNavios(self):
        # ler json e preencher as posicoes
        # atribuindo valor 10 a posicao preenchidas
        with open(filename) as dadosAtaque:
            dataClient = json.load(dadosAtaque)
            self.Tabuleiro()[dataClient['x']][dataClient['y']] = 10
        
        pass


logging.basicConfig()

USERS = set()

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def register(websocket):
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()


async def counter(websocket, path):

    global nome

    # register(websocket) sends user_event() to 
    await register(websocket)
    try:
        async for message in websocket:
            
            data = json.loads(message)
            
            print(data)
            
            if data['action'] == 'join':
                print('starting game...')
                nome = data['username']
                await asyncio.wait([websocket.send(json.dumps({ 'action': 'started' }))])
            
            elif data['action'] == 'sendBoard':
                print('init board with name ' + str(nome))

                player = Jogador(0,nome,data['board'])
            else:
                logging.error(
                    "unsupported event: {}", data)
    
    finally:
        await unregister(websocket)



asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, 'localhost', 8484)) # start server
asyncio.get_event_loop().run_forever()
