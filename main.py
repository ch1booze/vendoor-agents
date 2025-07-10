from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name='vendoor')


if __name__ == '__main__':
    mcp.run(transport='streamable-http')
