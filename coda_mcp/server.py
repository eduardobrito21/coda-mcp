from fastmcp import FastMCP

from coda_mcp.tools import register_tools

mcp = FastMCP(
    name="coda-mcp", instructions="Tools for reading and writing Coda docs, pages, and tables."
)

register_tools(mcp)


def main() -> None:
    """MCP over stdio (e.g. Cursor)."""
    mcp.run()


def main_http() -> None:
    """MCP over HTTP (e.g. cloud; API key via ``Authorization: Bearer``)."""
    mcp.run(transport="http")
