from contextlib import asynccontextmanager
from typing import Optional

import httpx
import mcp.types as types
from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel import Server
from openapi_specs import OpenAPISpec, get_openapi_specs


async def generate_tools() -> list[types.Tool]:
    openapi_specs: list[OpenAPISpec] = await get_openapi_specs()
    return [
        types.Tool(
            name=spec.operation_id,
            description=spec.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "default": spec.url},
                    "method": {"type": "string", "default": spec.method},
                    "params": {
                        "type": "array",
                        "items": {"type": "object"},
                        "default": spec.params or [],
                    },
                    "body": {"type": "object", "default": spec.body or {}},
                },
                "required": ["url", "method"],
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "response": {"type": "object", "default": spec.response or {}}
                },
            },
        )
        for spec in openapi_specs
    ]


class HTTPClient:
    async def request(
        self,
        url: str,
        method: str,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
    ):
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                url=url,
                params=params,
                json=body,
            )
            response.raise_for_status()
            return {"response": response.json()}


@asynccontextmanager
async def lifespan(_server: Server):
    http_client = HTTPClient()
    try:
        yield {"http_client": http_client}
    finally:
        pass


async def create_app():
    tools = await generate_tools()
    return FastMCP(name="vendoor", lifespan=lifespan, tools=tools)


if __name__ == "__main__":
    import asyncio

    app = asyncio.run(create_app())
    app.run(transport="streamable-http")
