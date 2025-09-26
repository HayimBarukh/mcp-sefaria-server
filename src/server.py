from mcp.server.sse import SseServerTransport
from mcp.server import Server

app = Server("sefaria-mcp")

# Регистрируем транспорт
transport = SseServerTransport("/sse")
app.include_router(transport.router)

# Vercel handler
handler = app.asgi_app
