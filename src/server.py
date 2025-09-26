# src/server.py
from mcp.server.fastmcp import FastMCP

# Создаём FastMCP MCP-сервер
mcp = FastMCP("sefaria")

# Healthcheck
@mcp.tool()
def ping() -> str:
    """Healthcheck endpoint for deployment sanity."""
    return "pong"

# Пример инструмента Sefaria (позже можно обернуть get_text/get_commentaries)
@mcp.tool()
def hello(name: str) -> str:
    """Test tool to ensure MCP connector is working."""
    return f"Hello, {name}!"

# FastMCP умеет автоматически отдавать manifest и capabilities
app = mcp.sse_app()
