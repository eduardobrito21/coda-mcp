from fastmcp import FastMCP

from .docs import register as register_docs
from .pages import register as register_pages
from .tables import register as register_tables


def register_tools(mcp: FastMCP) -> None:
    register_docs(mcp)
    register_pages(mcp)
    register_tables(mcp)
