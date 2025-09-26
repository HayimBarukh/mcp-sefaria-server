# src/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sefaria")

@mcp.tool()
def ping() -> str:
    return "pong"

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

# FastMCP уже умеет /sse, /manifest.json, /capabilities.json
app = mcp.sse_app()
