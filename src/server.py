# src/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sefaria")

@mcp.tool()
def ping() -> str:
    return "pong"

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

# Экспортируем FastAPI-приложение для Vercel
app = mcp.sse_app()
