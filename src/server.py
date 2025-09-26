# src/server.py
from src.sefaria_jewish_library.server import server as mcp_server
from mcp.server.sse import SseServerTransport

# Создаём SSE-транспорт и регистрируем MCP-сервер
transport = SseServerTransport("/sse")

# В некоторых версиях SDK требуется привязать сервер к транспорту:
# Если этот метод есть — оставляем строку, если нет — удаляем/комментируем.
try:
    transport.register_server(mcp_server)  # <-- если метод существует
except AttributeError:
    pass

# Vercel ищет переменную `app` (ASGI callable) на уровне модуля:
app = getattr(transport, "app", None) or getattr(transport, "asgi_app", None)

if app is None:
    # На случай, если у твоей версии SDK имя свойства другое
    raise RuntimeError("Cannot expose ASGI app from SseServerTransport; "
                       "tried .app and .asgi_app")
