from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import asyncio
import os
import logging
import sys
import json
from .sefaria_handler import * 

# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
       #  logging.FileHandler('sefaria_jewish_library.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('sefaria_jewish_library')

SSEFARIA_API_URL = "https://www.sefaria.org"



server = Server("sefaria_jewish_library")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    logger.debug("Handling list_tools request")
    return [
        types.Tool(
            name="get_text",
            description="get a jewish text from the jewish library",
            inputSchema={
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": "The reference of the jewish text, e.g. 'שולחן ערוך אורח חיים סימן א' or 'Genesis 1:1'",                               
                    },
                },
                "required": ["reference"],
            },
        ),
        types.Tool(
            name="get_commentaries",
            description="get a list of references of commentaries for a jewish text",
            inputSchema={
                "type": "object",
                "properties": {
                    "reference": {
                        "type": "string",
                        "description": "the reference of the jewish text, e.g. 'שולחן ערוך אורח חיים סימן א' or 'Genesis 1:1'",
                    },
                },
                "required": ["reference"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can search the Jewish library and return formatted results.
    """
    logger.debug(f"Handling call_tool request for {name} with arguments {arguments}")
    
    try:
        if not arguments:
            raise ValueError("Missing arguments")
    
        if name == "get_text":
            try:
                reference = arguments.get("reference")
                if not  reference:
                    raise ValueError("Missing reference parameter")  
                
                logger.debug(f"handle_get_text: {reference}")
                text = await get_text(reference)
                
                
                return [types.TextContent(
                    type="text",
                    text= text
                )]
            except Exception as err:
                logger.error(f"retreive text error: {err}", exc_info=True)
                return [types.TextContent(
                    type="text",
                    text=f"Error: {str(err)}"
                )]
                
              
        
        elif name == "get_commentaries":
            try:
                reference = arguments.get("reference")
                if not reference:
                    raise ValueError("Missing  parameter")
                logger.debug(f"handle_get_commentaries: {reference}")
                commentaries = await get_commentaries(reference)
                
                return [types.TextContent(
                    type="text",
                    text="\n".join(commentaries)
                )]
            except Exception as err:
                logger.error(f"retreive commentaries error: {err}", exc_info=True)
                return [types.TextContent(
                    type="text",
                    text=f"Error: {str(err)}"
                )]
           
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return [types.TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
    
async def main():
    try:
        logger.info("Starting Jewish Library MCP server...")
            
        # Run the server using stdin/stdout streams
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="sefaria_jewish_library",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise
