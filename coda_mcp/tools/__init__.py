from fastmcp import FastMCP

from .analytics import register as register_analytics
from .automations import register as register_automations
from .creation import register as register_creation
from .docs import register as register_docs
from .folders import register as register_folders
from .management import register as register_management
from .pages import register as register_pages
from .permissions import register as register_permissions
from .structure import register as register_structure
from .tables import register as register_tables


def register_tools(mcp: FastMCP) -> None:
    register_docs(mcp)
    register_permissions(mcp)
    register_pages(mcp)
    register_tables(mcp)
    register_structure(mcp)
    register_creation(mcp)
    register_management(mcp)
    register_folders(mcp)
    register_analytics(mcp)
    register_automations(mcp)
