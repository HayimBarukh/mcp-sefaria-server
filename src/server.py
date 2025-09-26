# src/server.py
# Vercel ищет переменную `app` (ASGI callable) на уровне модуля.

from mcp.server.fastmcp import FastMCP

# Инициализируем FastMCP-сервер
mcp = FastMCP("sefaria")

# (ВРЕМЕННЫЙ healthcheck-инструмент — чтобы убедиться, что сервер живёт)
@mcp.tool()
def ping() -> str:
    """Healthcheck endpoint for deployment sanity."""
    return "pong"

# Готовое ASGI-приложение для SSE-транспорта (по умолчанию путь /sse)
app = mcp.sse_app()
