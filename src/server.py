# src/server.py
# Vercel (Python) ожидает ASGI-callable с именем `app` на уровне модуля.
# FastMCP даёт готовое ASGI-приложение для SSE: mcp.sse_app()

from mcp.server.fastmcp import FastMCP

# Создаём FastMCP-сервер
mcp = FastMCP("sefaria")

# --- Подключаем твои функции из sefaria_handler ---
# Примечание: в твоём handler `get_text` и `get_commentaries` — async.
from src.sefaria_jewish_library.sefaria_handler import (
    get_text,          # async def get_text(reference: str) -> str
    get_commentaries,  # async def get_commentaries(reference: str) -> list[str]
)

# Простой healthcheck (помогает убедиться, что сервер жив)
@mcp.tool()
def ping() -> str:
    """Deployment healthcheck."""
    return "pong"

# Обёртка MCP-инструмента для получения текста по ref
@mcp.tool()
async def sefaria_text(reference: str) -> str:
    """
    Get text from Sefaria by textual reference, e.g. 'Genesis 1:1' or 'בראשית א:א'.
    Returns plain text (Hebrew by default in your handler).
    """
    result = await get_text(reference)
    # handler возвращает str; на всякий случай приводим к строке
    return result if isinstance(result, str) else str(result)

# Обёртка MCP-инструмента для получения комментариев по ref
@mcp.tool()
async def sefaria_commentaries(reference: str) -> str:
    """
    Get list of commentary refs for a given reference and return as newline-separated text.
    """
    items = await get_commentaries(reference)
    if not items:
        return ""
    # mcp текстовый ответ; склеим списком
    return "\n".join(items)

# Создаём ASGI-приложение (SSE endpoint /sse)
app = mcp.sse_app()
