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
    
    
    def checkPosition(self,player,coodX,coodY):

        if player.board[coodX][coodY] == 0:
            return "Errou"
        elif player.board[coodX][coodY] == 'X' or player.board[coodX][coodY] == 'O':
            # Nao pode jogar nessas coordenadas
            return "Invalido"
        else:
            # Acertou o navio
            return "Acertou"

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
    
    print("numero de usuarios:" + str(USERS))
    
    if len(USERS) == 2:
        # Iniciar o jogo com player1 e player 2
        # game = Jogo(player1,player2)
        print("Podemos Comecar!")
    else:
        # congleado conexao
        pass

    
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

                player = Jogador(0,nome,data['board'],websocket)

                player.tabuleiro(9,9)
                player.tabuleiro(9,8)
                #quadro = Quadro(data['board'])
                print(player.board)
            else:
                logging.error(
                    "unsupported event: {}", data)
    finally:
        await unregister(websocket)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, 'localhost', 8484)) # start server
asyncio.get_event_loop().run_forever()
