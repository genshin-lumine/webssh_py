import asyncssh
from app.ssh.session import WebSSHClientSession


# SSH 客户端连接
async def create_ssh_connection(
    ws, host, username, password=None, port=22, client_keys=None, passphrase=None):
    conn = await asyncssh.connect(
        host,
        username=username,
        password=password,
        port=port,
        known_hosts=None,
        client_keys=client_keys,
        passphrase=passphrase
        )
    chan, session = await conn.create_session(
        lambda: WebSSHClientSession(ws), term_type='xterm-256color',
        term_size=(80, 24)
    )
    
    async def ws_to_ssh():
        async for msg in ws:
            chan.write(msg.data)
    
    return conn, chan, session, ws_to_ssh