import asyncio
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP
from app.openapi import OpenAPISpec, get_openapi_specs

app = FastMCP(name="vendoor", stateless_http=False)


async def add_tools():
    openapi_specs: list[OpenAPISpec] = await get_openapi_specs()
    for spec in openapi_specs:

        @app.tool(name=spec.operation_id, description=spec.description)
        async def tool_function(
            params: Optional[dict] = None,
            body: Optional[dict] = None,
        ):
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=spec.method,
                    url=spec.url,
                    params=params,
                    json=body,
                )
                response.raise_for_status()
                return response.json()


asyncio.run(add_tools())

if __name__ == "__main__":
    app.run(transport="streamable-http")
