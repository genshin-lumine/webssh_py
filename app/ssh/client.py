import asyncssh
from app.ssh.session import WebSSHClientSession
import json


# SSH 客户端连接
async def create_ssh_connection(
    ws, host, username, password=None, port=22, client_keys=None, passphrase=None, cols=80, rows=24):
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
        term_size=(cols, rows)
    )
    
    async def ws_to_ssh():
        async for msg in ws:
            # 先尝试按 JSON 控制消息解析（如 resize）
            try:
                ctrl = json.loads(msg.data)
                if isinstance(ctrl, dict) and ctrl.get('type') == 'resize':
                    chan.change_terminal_size(ctrl['cols'], ctrl['rows'])
                    continue
            except json.JSONDecodeError:
                pass
            # 不是控制消息 -> 普通按键，转发给 SSH
            chan.write(msg.data)
    
    return conn, chan, session, ws_to_ssh