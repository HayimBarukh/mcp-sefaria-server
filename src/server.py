import asyncio
from mcp.server.sse import SseServerTransport  # ← правильное имя

from src.sefaria_jewish_library.server import server as mcp_server

async def main():
    transport = SseServerTransport("/sse")  # ← тоже SseServerTransport
    await mcp_server.run(transport)

if __name__ == "__main__":
    asyncio.run(main())
