import os
from aiohttp import web


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..','templates')


async def index_handler(request):
    with open(os.path.join(TEMPLATE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        html_content = f.read()
    return web.Response(content_type='text/html', text=html_content)