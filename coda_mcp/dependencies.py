"""Coda API auth for MCP tools — use ``CodaApiKeyDependency`` on each tool."""

from fastmcp.dependencies import Depends
from fastmcp.exceptions import ToolError
from fastmcp.server.dependencies import get_http_headers, get_http_request

from coda_mcp.config import settings


def get_coda_api_key() -> str:
    """Resolve the Coda API key.

    **HTTP**

    1. ``X-Coda-Api-Key`` header (best for clients that support it).
    2. ``coda_api_key`` query parameter.
    3. Server ``CODA_API_KEY`` env
        — only if ``CODA_MCP_HTTP_ALLOW_ENV_API_KEY`` is true (default is False)

    **Stdio** (local Cursor, etc.):

    - ``CODA_API_KEY`` in the process environment only; headers/query are unused.
    """

    headers = get_http_headers()
    coda_api_key = headers.get("x-coda-api-key", "").strip()
    if coda_api_key:
        return coda_api_key

    try:
        request = get_http_request()
    except RuntimeError:
        request = None

    if request is not None:
        coda_api_key = request.query_params.get("coda_api_key", "").strip()
        if coda_api_key:
            return coda_api_key

        if settings.coda_mcp_http_allow_env_api_key and settings.coda_api_key is not None:
            return settings.coda_api_key.get_secret_value()

        raise ToolError(
            "No Coda API key for this request. Send header X-Coda-Api-Key or set query parameter coda_api_key to the MCP URL, "
        )

    if settings.coda_api_key is not None:
        return settings.coda_api_key.get_secret_value()

    raise ToolError(
        "No Coda API key found. Set CODA_API_KEY for local stdio, or use HTTP with X-Coda-Api-Key or query parameter coda_api_key."
    )


# Shared ``Depends`` instance — use as: ``coda_api_key: str = CodaApiKeyDependency``
CodaApiKeyDependency = Depends(get_coda_api_key)
