from app.handlers.index import index_handler
from app.handlers.websocket import websocket_handler
from app.handlers.login import login_handler

def setup_routes(app):
    app.router.add_get('/', index_handler)
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/login', login_handler)