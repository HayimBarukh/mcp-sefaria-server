from mcp.server.fastmcp import FastMCP

# создаём сервер
mcp = FastMCP("sefaria")

@mcp.tool()
def ping() -> str:
    return "pong"

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

# SSE-приложение для Vercel
app = mcp.sse_app()
