from websockets.sync.client import connect
from threading import Thread, Event

terminate = Event()
username = input('Enter username: ')

# -- reader
def read(ws):
    while not terminate.is_set():
        try:
            msg = ws.recv(timeout=1)
            print('{}\n> '.format(msg), end='')
        except TimeoutError: continue
        except Exception as e:
            print('Error: {}'.format(e))
            terminate.set()

# --
def writer():
    with connect("ws://localhost:8765") as websocket:
        reader = Thread(target=read, args=(websocket,))
        reader.start()
        websocket.send('username:{}'.format(username))
        while True:
            message = input('> ')
            if message.lower() == 'q':
                break
            websocket.send(message)
        # -- wait for reader
        terminate.set()
        reader.join()

if __name__ == '__main__':
    writer()

