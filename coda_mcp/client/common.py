from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from coda_mcp.validation import validate_pydantic_as_cast

# Values ``httpx`` accepts as query parameters (from ``model_dump(by_alias=True, exclude_none=True)``).
type _QueryPrimitive = str | int | float | bool
type QueryParamMap = dict[str, _QueryPrimitive | list[_QueryPrimitive]]


class CodaRequestMixin:
    """Shared HTTP surface for Coda API subclients."""

    http: httpx.AsyncClient
    base_url: str

    def url(self, path: str) -> str:
        base = self.base_url.rstrip("/") + "/"
        return urljoin(base, path.removeprefix("/"))

    def query_dict(self, params: BaseModel | None) -> QueryParamMap:
        if params is None:
            return {}
        raw = params.model_dump(by_alias=True, exclude_none=True)
        return validate_pydantic_as_cast(QueryParamMap, raw)
