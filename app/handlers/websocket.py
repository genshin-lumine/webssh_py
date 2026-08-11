from aiohttp import web
from app.ssh.client import create_ssh_connection

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    try:
        conn, chan, session, ws_to_ssh = await create_ssh_connection(
            ws, 'localhost', 'dasg', '14212xsagy')
        await ws_to_ssh()
    except Exception as e:
        print(f'SSH 连接失败: {e}')
        await ws.send_str(f'\r\n[连接失败: {e}]\r\n')
        await ws.close()
    return ws