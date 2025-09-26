from sefaria_jewish_library.sefaria_handler import create_server
from mcp.server.sse import SSEServerTransport
import asyncio

async def main():
    server = create_server()
    transport = SSEServerTransport("/sse")
    await server.run(transport)

if __name__ == "__main__":
    asyncio.run(main())
