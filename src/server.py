from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Создаём MCP сервер
mcp = FastMCP("sefaria")

@mcp.tool()
def ping() -> str:
    return "pong"

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

# Создаём FastAPI app
app = FastAPI()

# Подключаем SSE (чтобы /sse работал)
sse_app = mcp.sse_app()
app.mount("/", sse_app)

# Явно создаём /manifest.json
@app.get("/manifest.json")
def manifest():
    return JSONResponse(mcp.get_manifest())

# Явно создаём /capabilities.json
@app.get("/capabilities.json")
def capabilities():
    return JSONResponse(mcp.get_capabilities())
