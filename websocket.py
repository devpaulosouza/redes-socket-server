import asyncio
import json
import logging
import websockets
import uuid

logging.basicConfig()

USERS = set()

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
    USERS.add(websocket)
    await notify_users()

async def unregister(websocket):
    USERS.remove(websocket)
    await notify_users()

async def counter(websocket, path):
    # register(websocket) sends user_event() to 
    websocket.uuid = uuid.uuid4()
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(data)
            if data['action'] == 'join':
                print('joining game...')
                await start_game(websocket)
            if data['action'] == 'sendBoard':
                print('board: ' + str(data['board']))
            else:
                logging.error(
                    "unsupported event: {}", data)
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, 'localhost', 8484))
asyncio.get_event_loop().run_forever()
