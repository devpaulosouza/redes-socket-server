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
import uuid


######################################################################################################
#                                               Class Jogo                                           #
######################################################################################################
# Matriz possue posicoes zeradas, ou seja campo vazio,
# valor O para as posicoes que foram acertadas e X para as erradas
#
######################################################################################################

class Jogo:
    
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player2
        self.shipsPlayer1 = []
        self.shipsPlayer2 = []
        self.attackedBlocksPlayer1 = []
        self.attackedBlocksPlayer2 = []


    def checkResult(self,player):

        if player.life == 30: player.socket.send("Parabens, você venceu :D")
        else: player.socket.send("Você perdeu :(")
    
    # Funcao para atualizar o tabuleiro do player
    # param player
    # param coodX
    # param coodY 
    def checkPosition(self,player,coodX,coodY):

        if player.board[coodX][coodY] == 0:
            return "Errou"
        elif player.board[coodX][coodY] == 'X' or player.board[coodX][coodY] == 'O':
            # Nao pode jogar nessas coordenadas
            return "Invalido"
        else:
            # Acertou o navio
            return "Acertou"

    # Funcao para atualizar o tabuleiro do player
    # param player
    # param coodX
    # param coodY
    def upDatePosition(self,player,coodX,coodY):
        player.tabuleiro(coodX,coodY)

    def startGame(self):
        # Se acertou mando mensagem e continua a jogada
        # caso errou manda mensagem, colore posicao e muda de jogador
        
        
        #await websockets.send("Jogo Iniciado")

        self.player1.socket.send("Joga")
        # Condicao, quem acertar todos os navios primeiro vence
        """if inimigo == 30:
            response = "Que pena, você perdeu!\n" 
            websockets.send(str.encode(response))
        else:
            response = "Parabéns! Você ganhou!\n" 
            websockets.send(str.encode(response))"""
        
        pass


######################################################################################################
#                                             Class Jogador                                          #
######################################################################################################

class Jogador:
    
    def __init__(self, id, nome,board,webSocket):
        self.id = id
        self.name = nome
        self.board = board
        self.socket = webSocket
        self.life = 0 # vai ate 30

    # Funcao para atualizar o Tabuleiro do player
    # param coodX   Recebe valor inteiro da coordenada de X
    # param coodY'  Recebe valor inteiro da coordenada de X
    def tabuleiro(self,coodX,coodY):

        if self.board[coodX][coodY] == 0:
            self.board[coodX][coodY] = "X"
        elif (self.board[coodX][coodY] != 0 and not self.board[coodX][coodY] == "X") or (self.board[coodX][coodY] != 0 and not self.board[coodX][coodY] == "O"):
            self.board[coodX][coodY] = "O"
        else:
            print("Essa posicao ja foi marcada")

######################################################################################################

logging.basicConfig()

USERS = []

def users_event():
    return json.dumps({'type': 'users', 'count': len(USERS)})

async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])

async def start_game(user):
    if len(USERS) % 2 == 0:
        await asyncio.wait([u.send(json.dumps({ 'action': 'started', 'uuid': str(u.uuid) })) for u in USERS])
    else:
        await asyncio.wait([user.send(json.dumps({ 'action': 'waitingOtherPlayer', 'uuid': str(user.uuid) }))])

async def register(websocket):
    USERS.append(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def send_message(websocket, action, data = None):
    print(data)
    await asyncio.wait([websocket.send(json.dumps({ 'action': action, 'data': data }))])


players = 0


async def counter(websocket, path):
    websocket.uuid = uuid.uuid4()

    await register(websocket)
    
    try:
        async for message in websocket:
            
            data = json.loads(message)
            
            print(data)
            
            if data['action'] == 'join':
                if len(USERS) == 1:
                    USERS[0].username = data['username']
                    await send_message(USERS[0], 'waitingOtherPlayer')
                    
                elif len(USERS) == 2:
                    USERS[1].username = data['username']
                    await send_message(USERS[0], 'started', { 'username': USERS[1].username })
                    await send_message(USERS[1], 'started', { 'username': USERS[0].username })

            elif data['action'] == 'sendBoard':
                pass
            else:
                logging.error(
                    "unsupported event: {}", data)
    finally:
        pass


asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, 'localhost', 8484)) # start server
asyncio.get_event_loop().run_forever()
