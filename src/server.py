# src/server.py
# Vercel (Python) ждёт на уровне модуля переменную `app` — ASGI-приложение.
# FastMCP умеет сам отдавать ASGI-app для SSE через .sse_app()

from mcp.server.fastmcp import FastMCP

# создаём FastMCP-сервер
mcp = FastMCP("sefaria")

# healthcheck-инструмент (полезно для быстрой проверки)
@mcp.tool()
def ping() -> str:
    return "pong"

# ASGI-приложение с SSE-эндпоинтом (по умолчанию путь /sse)
app = mcp.sse_app()
