from typing import Literal, Optional
import httpx
from environment import OPENAPI_JSON_URL
from pydantic import BaseModel, create_model


class APIRequestSchema(BaseModel):
    url: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    operation_id: str
    description: str
    params: Optional[list[dict]] = None
    request_body: Optional[dict] = None
    response: Optional[dict] = None


async def fetch_openapi_spec():
    async with httpx.AsyncClient() as client:
        response = await client.get(OPENAPI_JSON_URL)
        response.raise_for_status()
        openapi_spec = response.json()
    return openapi_spec

def create_pydantic_model_from_schema(schema):
    ...


def resolve_openapi_spec(openapi_spec: dict):
    def resolve_schema_refs(schema):
        if isinstance(schema, dict):
            return {key: resolve_schema_refs(value) for key, value in schema.items()}
        elif isinstance(schema, str) and schema.startswith("#/components"):
            schema_name = schema.split("/")[-1]
            schema_object = openapi_spec["components"]["schemas"].get(schema_name)
            return {"name": schema_name, "schema": schema_object}
        else:
            return schema

    api_request_schemas = list()
    paths = openapi_spec.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            tags = details.get("tags", [])
            if "Customer-Agent" in tags:
                if request_body_schema := (
                    openapi_spec["paths"][path][method]
                    .get("requestBody", {})
                    .get("content", {})
                    .get("application/json", {})
                    .get("schema")
                ):
                    request_body_schema = resolve_schema_refs(request_body_schema)

                if response_schema := openapi_spec["paths"][path][method].get(
                    "responses"
                ):
                    response_schema = next(iter(response_schema.values()))
                    response_schema = (
                        response_schema.get("content")
                        .get("application/json", {})
                        .get("schema")
                    )
                    response_schema = resolve_schema_refs(response_schema)

                api_request_schemas.append(
                    APIRequestSchema(
                        url=path,
                        method=method.upper(),
                        operation_id=details.get("operationId", ""),
                        description=details.get("description", ""),
                        params=details.get("parameters", []),
                    )
                )


if __name__ == "__main__":
    import asyncio

    openapi_spec = asyncio.run(fetch_openapi_spec())
    resolved_specs = resolve_openapi_spec(openapi_spec)
    print(resolved_specs)
