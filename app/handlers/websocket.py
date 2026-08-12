from aiohttp import web
from app.ssh.client import create_ssh_connection
import json
from app.auth import build_auth_params


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    try:
        msg = await ws.receive()
        data = json.loads(msg.data)
        print(f'验证方式: {data["auth_type"]}')
        
        # 公共参数
        common = {
            "ws": ws,
            "host": data["host"],
            "username": data["username"],
            "port": data.get("port", 22)
        }
        # 根据认证方式构建连接参数
        auth_params = build_auth_params(data)
        conn, chan, session, ws_to_ssh = await create_ssh_connection(
            **common, **auth_params,
            cols=data.get("cols", 80),
            rows=data.get("rows", 24)
        )
        await ws_to_ssh()
    except Exception as e:
        print(f'SSH 连接失败: {e}')
        await ws.send_str(f'\r\n[连接失败: {e}]\r\n')
        await ws.close()
    return ws