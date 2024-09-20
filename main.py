import asyncio
from websockets.asyncio.server import serve

clients = dict()

async def echo(websocket):
    handshake = await websocket.recv()
    try:
        username = handshake.split(':')[-1].strip()
        print('{}:{} connected as {}'.format(*websocket.remote_address, username))
        clients[username] = websocket
        # -- enter notice
        for ws in clients.values():
            if ws == websocket: continue
            await ws.send('{} has entered chatroom.'.format(username))
    except Exception: return
    try:
        async for message in websocket:
            for ws in clients.values():
                if ws == websocket: continue
                await ws.send('[{}]: {}'.format(username, message))
    except Exception:
        print('{} exited.'.format(username))
    finally:
        clients.pop(username)
        try: # exit notice
            for ws in clients.values():
                if ws == websocket: continue
                await ws.send('{} left the room'.format(username))
        except: pass

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())

