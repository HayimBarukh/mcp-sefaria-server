import asyncio
from mcp.server.sse import SseServerTransport  # <-- верное имя класса

# Берём готовый экземпляр MCP-сервера из пакета
from src.sefaria_jewish_library.server import server as mcp_server

async def main():
    transport = SseServerTransport("/sse")  # <-- корректный класс
    await mcp_server.run(transport)

if __name__ == "__main__":
    asyncio.run(main())
