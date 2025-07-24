from typing import Literal, Optional

import httpx
import jsonref
from environment import OPENAPI_JSON_URL
from pydantic import BaseModel


class OpenAPISpec(BaseModel):
    url: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    operation_id: str
    description: str
    params: Optional[list[dict]] = None
    body: Optional[dict] = None
    response: Optional[dict] = None


async def get_openapi_specs() -> list[OpenAPISpec]:
    specs = list()

    async with httpx.AsyncClient() as client:
        response = await client.get(OPENAPI_JSON_URL)
        response.raise_for_status()
        openapi_json = response.json()
        openapi_jsonref = jsonref.replace_refs(openapi_json)

    paths = openapi_jsonref.get("paths", {})
    for route, methods in paths.items():
        for method, details in methods.items():
            tags = details.get("tags", [])
            if "Customer-Agent" in tags:
                specs.append(
                    OpenAPISpec(
                        url=route,
                        method=method.upper(),
                        operation_id=details.get("operationId", ""),
                        description=details.get("description", ""),
                        params=details.get("parameters", []),
                        body=details.get("requestBody", {})
                        .get("content", {})
                        .get("application/json", {})
                        .get("schema", {}),
                        response=details.get("responses", {})
                        .get("200", {})
                        .get("content", {})
                        .get("application/json", {})
                        .get("schema", {}),
                    )
                )

    return specs


if __name__ == "__main__":
    import asyncio

    asyncio.run(get_openapi_specs())
