from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.responses import JSONResponse

mcp = FastMCP("sefaria")

@mcp.tool()
def ping() -> str:
    return "pong"

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

# Создаём FastAPI-приложение
app = FastAPI()

# Подключаем SSE-роуты от MCP
sse_app = mcp.sse_app()
app.mount("/", sse_app)

# Явно добавляем manifest.json и capabilities.json
@app.get("/manifest.json")
def manifest():
    return JSONResponse(mcp.get_manifest())

@app.get("/capabilities.json")
def capabilities():
    return JSONResponse(mcp.get_capabilities())
