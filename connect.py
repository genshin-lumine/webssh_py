import asyncio
import asyncssh
from aiohttp import web


async def index_handler(request):
    return web.Response(
        content_type='text/html',
        text="""<!DOCTYPE html>
                    <html>
                    <head>
                        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@4.19.0/css/xterm.css" />
                    </head>
                    <body>
                        <div id="terminal" style="height:100vh"></div>
                        <script src="https://cdn.jsdelivr.net/npm/xterm@4.19.0/lib/xterm.js"></script>
                        <script>
                            const term = new Terminal({ rows: 30, cols: 100 });
                            term.open(document.getElementById('terminal'));
                            const ws = new WebSocket('ws://localhost:8080/ws');
                            term.onData(data => ws.send(data));
                            ws.onmessage = e => term.write(e.data);
                        </script>
                    </body>
                    </html>"""
                        )

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    class MySSHClientSession(asyncssh.SSHClientSession):
        def data_received(self, data, datatype):
            asyncio.ensure_future(ws.send_str(data))

        def connection_lost(self, exc):
            if exc:
                print(f'Connection lost: {exc}')
            else:
                print('Connection closed.')
    try:
        # 建立SSH链接
        async with asyncssh.connect('localhost', username='dasg', password='14212xsagy', known_hosts=None) as conn:
            chan, session = await conn.create_session(
                lambda: MySSHClientSession(), term_type='xterm-256color',
                term_size=(80, 24)
            )
            
            async def ws_to_ssh():
                async for msg in ws:
                    chan.write(msg.data)
            await asyncio.gather(ws_to_ssh())
    except Exception as e:
            print(f'SSH 连接失败: {e}')
            await ws.send_str(f'\r\n[连接失败: {e}]\r\n')
            await ws.close()
        
    return ws




app = web.Application()
app.router.add_get('/', index_handler)
app.router.add_get('/ws', websocket_handler)
web.run_app(app)


