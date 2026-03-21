from fastmcp import FastMCP

from coda_mcp.tools import register_tools

mcp = FastMCP(
    name="coda-io-mcp", instructions="Tools for reading and writing Coda docs, pages, and tables."
)

register_tools(mcp)


def main() -> None:
    mcp.run()
