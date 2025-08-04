import asyncio
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP
from openapi import APISchema, load_api_schemas
from pydantic import ValidationError

app = FastMCP(name="vendoor", stateless_http=False)


async def add_tools():
    api_schemas: list[APISchema] = await load_api_schemas()
    for schema in api_schemas:
        @app.tool(name=schema.operation_id, description=schema.description)
        async def tool_function(
            params: Optional[dict] = None,
            body: Optional[dict] = None,
        ):
            if body and schema.request_body_model:
                try:
                    request_body_model = schema.request_body_model
                    request_body_model(**body)
                except ValidationError as e:
                    return e

            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=schema.method,
                    url=schema.url,
                    params=params,
                    json=body,
                )
                response.raise_for_status()
                response_data = response.json()

                if schema.response_model:
                    try:
                        response_model = schema.response_model
                        response_model(**response_data)
                    except ValidationError as e:
                        return e

                return response_data


asyncio.run(add_tools())

app.run(transport="streamable-http")
