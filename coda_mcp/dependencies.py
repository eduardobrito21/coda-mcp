"""Coda API auth for MCP tools — use ``CodaApiKeyDependency`` on each tool."""

from fastmcp.dependencies import Depends
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers

from coda_mcp.config import settings


def get_coda_api_key() -> str:
    """Resolve the Coda API key.

    HTTP: read ``X-Coda-Api-Key`` (not ``Authorization``, which the platform may use).

    Stdio / no request: use ``CODA_API_KEY`` from the environment.
    """
    headers = get_http_headers()
    from_header = headers.get("x-coda-api-key", "").strip()
    if from_header:
        return from_header

    if settings.coda_api_key is not None:
        return settings.coda_api_key.get_secret_value()

    raise ToolError("No Coda API key found")


# Shared ``Depends`` instance — use as: ``coda_api_key: str = CodaApiKeyDependency``
CodaApiKeyDependency = Depends(get_coda_api_key)
