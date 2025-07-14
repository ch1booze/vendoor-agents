import json

import httpx
from environment import OPENAPI_JSON_URL


async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get(OPENAPI_JSON_URL)
        response.raise_for_status()
        openapi_json = response.json()

    paths = openapi_json.get("paths", {})
    for route, methods in paths.items():
        for method, details in methods.items():
            tags = details.get("tags", [])
            if "Customer-Agent" in tags:
                print(f"Route: {route}, Method: {method.upper()}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
