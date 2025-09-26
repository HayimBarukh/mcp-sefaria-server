# src/server.py
from mcp.server.fastmcp import FastMCP

# Создаём MCP-сервер
mcp = FastMCP("sefaria")

# Healthcheck
@mcp.tool()
def ping() -> str:
    """Healthcheck endpoint for deployment sanity."""
    return "pong"

# Пример инструмента
@mcp.tool()
def hello(name: str) -> str:
    """Test tool to ensure MCP connector is working."""
    return f"Hello, {name}!"

# FastMCP автоматически создаёт endpoints:
#  - /sse
#  - /manifest.json
#  - /capabilities.json
app = mcp.sse_app()

# Для Vercel нужно явно экспортировать handler
handler = app
