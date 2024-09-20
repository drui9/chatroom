from unittest import TestCase
from websockets.sync.client import connect

# --
class TestChatroom(TestCase):
    def test_echo(self):
        with connect("ws://localhost:8765") as websocket:
            username = 'username:test_client'
            websocket.send(username)
            # --
            message = "Hello, world!"
            websocket.send(message)
            rep = websocket.recv()
            print(rep)
            assert rep == message

