import asyncio
import asyncssh

class WebSSHClientSession(asyncssh.SSHClientSession):
    def __init__(self, ws):
        self.ws = ws
    
    def data_received(self, data, datatype):
        asyncio.ensure_future(self.ws.send_str(data))

    def connection_lost(self, exc):
        if exc:
            print(f'Connection lost: {exc}')
        else:
            print('Connection closed.')
