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
# valor 9 para as posicoes que foram acertadas
#
######################################################################################################

class Jogo:
    
    def __init__(self,player1,player2):
        self.player1 = player1
        self.player2 = player
        self.shipsPlayer1 = []
        self.shipsPlayer2 = []
        self.attackedBlocksPlayer1 = []
        self.attackedBlocksPlayer2 = []


    def verificaResultado(self):
        if len(reduce(lambda x,y : x+y, self.shipsPlayer1)) == len(self.attackedBlocksPlayer1):
            return self.player2 , self.player1
        if len(reduce(lambda x,y : x+y, self.shipsPlayer2)) == len(self.attackedBlocksPlayer2):
            return self.player1 , self.player2

        return None , None
    
    
    def verificaPosicao(self,player,coodX,coodY):

        if player.board[coodX][coodY] != 0 or player.board[coodX][coodY] != '*':
            # atualizar tabuleiro
            player.tabuleiro(coodX,coodY)
            return True
        else:
            return False

    
    
    def startGame(self):
        # Se acertou mando mensagem e continua a jogada
        # caso errou manda mensagem, colore posicao e muda de jogador
        
        
        #await websockets.send("Jogo Iniciado")


        # Condicao
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


    def tabuleiro(self,coodX,coodY):
        # Atualizar tabuleiro
        
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
