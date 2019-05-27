import asyncio
import json
import logging
import websockets

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
    # register(websocket) sends user_event() to 
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(data)
            if data['action'] == 'start':
                print('starting game...')
                await asyncio.wait([websocket.send(json.dumps({ 'action': 'started' }))])
            else:
                logging.error(
                    "unsupported event: {}", data)
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, 'localhost', 8484))
asyncio.get_event_loop().run_forever()
