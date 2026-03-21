from fastmcp import FastMCP

from .creation import register as register_creation
from .docs import register as register_docs
from .management import register as register_management
from .pages import register as register_pages
from .structure import register as register_structure
from .tables import register as register_tables


def register_tools(mcp: FastMCP) -> None:
    register_docs(mcp)
    register_pages(mcp)
    register_tables(mcp)
    register_structure(mcp)
    register_creation(mcp)
    register_management(mcp)
