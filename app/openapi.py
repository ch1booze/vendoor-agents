from datetime import datetime
from typing import Any, Literal, Optional

import httpx
from environment import OPENAPI_JSON_URL
from pydantic import BaseModel, Field, create_model


class APISchema(BaseModel):
    url: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    operation_id: str
    description: str
    params: Optional[list[dict]] = None
    request_body_model: Optional[Any] = None
    response_model: Optional[Any] = None


async def fetch_openapi_spec():
    async with httpx.AsyncClient() as client:
        response = await client.get(OPENAPI_JSON_URL)
        response.raise_for_status()
        openapi_spec = response.json()
    return openapi_spec


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

    json_type_map = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "object": dict,
        "array": list,
    }

    def create_pydantic_model_from_schema(schema: dict):
        if schema.get("type") == "array":
            item_schema = schema.get("items", {})
            item_model = create_pydantic_model_from_schema(item_schema)
            return list[item_model]

        if "$ref" in schema:
            ref_details = schema["$ref"]
            model_name = ref_details.get("name", "DynamicModel")
            object_schema = ref_details.get("schema", {})

            if object_schema.get("type") != "object":
                raise ValueError("Schema inside $ref must be of type 'object'")

            properties = object_schema.get("properties", {})
            required_fields = object_schema.get("required", [])

            pydantic_fields = {}

            for field_name, field_props in properties.items():
                field_type_str = field_props.get("type")

                if (
                    field_props.get("format") == "date-time"
                    and field_type_str == "string"
                ):
                    python_type = datetime
                else:
                    python_type = json_type_map.get(field_type_str, any)

                field_args = {
                    "description": field_props.get("description"),
                    "example": field_props.get("example"),
                }

                if field_name not in required_fields:
                    python_type = Optional[python_type]
                    field_args["default"] = field_props.get("default")
                else:
                    if "default" in field_props:
                        field_args["default"] = field_props.get("default")
                    else:
                        field_args["default"] = ...

                clean_field_args = {
                    k: v for k, v in field_args.items() if v is not None
                }

                pydantic_fields[field_name] = (python_type, Field(**clean_field_args))
                DynamicModel = create_model(model_name, **pydantic_fields)
                return DynamicModel

        raise ValueError(
            "Unsupported schema structure. Expected 'type: array' or '$ref'."
        )

    api_schemas = list()
    paths = openapi_spec.get("paths", {})
    for path, methods in paths.items():
        for method, details in methods.items():
            tags = details.get("tags", [])
            if "Customer-Agent" in tags:
                api_schema = APISchema(
                    url=path,
                    method=method.upper(),
                    operation_id=details.get("operationId", ""),
                    description=details.get("description", ""),
                    params=details.get("parameters", []),
                )

                if request_body_schema := (
                    openapi_spec["paths"][path][method]
                    .get("requestBody", {})
                    .get("content", {})
                    .get("application/json", {})
                    .get("schema")
                ):
                    request_body_schema = resolve_schema_refs(request_body_schema)
                    request_body_model = create_pydantic_model_from_schema(
                        request_body_schema
                    )
                    api_schema.request_body_model = request_body_model

                if response_schema := openapi_spec["paths"][path][method].get(
                    "responses"
                ):
                    response_schema = next(iter(response_schema.values()))
                    response_schema = (
                        response_schema.get("content", {})
                        .get("application/json", {})
                        .get("schema")
                    )
                    response_schema = resolve_schema_refs(response_schema)
                    response_model = create_pydantic_model_from_schema(response_schema)
                    api_schema.response_model = response_model

                api_schemas.append(api_schema)

    return api_schemas


async def load_api_schemas():
    return resolve_openapi_spec(await fetch_openapi_spec())
