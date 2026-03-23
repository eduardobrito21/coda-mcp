from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.http_errors import raise_coda_http_error
from coda_mcp.models import (
    AnalyticsUpdatedResponse,
    DocAnalyticsListQuery,
    DocAnalyticsListResponse,
    DocAnalyticsSummaryQuery,
    DocAnalyticsSummaryResponse,
    MutationStatusResponse,
    PackAnalyticsListQuery,
    PackAnalyticsListResponse,
    PackAnalyticsSummaryQuery,
    PackAnalyticsSummaryResponse,
    PackFormulaAnalyticsListResponse,
    PackFormulaAnalyticsQuery,
    PageAnalyticsListQuery,
    PageAnalyticsListResponse,
    ResolveBrowserLinkQuery,
    ResolveBrowserLinkResponse,
    WhoamiResponse,
)
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class MiscellaneousClient(CodaRequestMixin):
    """Account, analytics, resolve link, mutation status ([Coda API — Miscellaneous](https://coda.io/developers/apis/v1#))."""

    http: httpx.AsyncClient
    base_url: str

    async def get_whoami(self, *, api_key: str) -> WhoamiResponse:
        response = await self.http.get(
            self.url("/whoami"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(WhoamiResponse, response.json())

    async def get_resolve_browser_link(
        self, query: ResolveBrowserLinkQuery, *, api_key: str
    ) -> ResolveBrowserLinkResponse:
        response = await self.http.get(
            self.url("/resolveBrowserLink"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(ResolveBrowserLinkResponse, response.json())

    async def get_mutation_status(self, request_id: str, *, api_key: str) -> MutationStatusResponse:
        response = await self.http.get(
            self.url(f"/mutationStatus/{quote(request_id, safe='')}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(MutationStatusResponse, response.json())

    async def get_doc_analytics(
        self, query: DocAnalyticsListQuery | None = None, *, api_key: str
    ) -> DocAnalyticsListResponse:
        response = await self.http.get(
            self.url("/analytics/docs"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DocAnalyticsListResponse, response.json())

    async def get_page_analytics(
        self,
        doc_id: str,
        query: PageAnalyticsListQuery | None = None,
        *,
        api_key: str,
    ) -> PageAnalyticsListResponse:
        response = await self.http.get(
            self.url(f"/analytics/docs/{quote(doc_id, safe='')}/pages"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PageAnalyticsListResponse, response.json())

    async def get_doc_analytics_summary(
        self,
        query: DocAnalyticsSummaryQuery | None = None,
        *,
        api_key: str,
    ) -> DocAnalyticsSummaryResponse:
        response = await self.http.get(
            self.url("/analytics/docs/summary"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DocAnalyticsSummaryResponse, response.json())

    async def get_pack_analytics(
        self, query: PackAnalyticsListQuery | None = None, *, api_key: str
    ) -> PackAnalyticsListResponse:
        response = await self.http.get(
            self.url("/analytics/packs"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PackAnalyticsListResponse, response.json())

    async def get_pack_analytics_summary(
        self,
        query: PackAnalyticsSummaryQuery | None = None,
        *,
        api_key: str,
    ) -> PackAnalyticsSummaryResponse:
        response = await self.http.get(
            self.url("/analytics/packs/summary"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PackAnalyticsSummaryResponse, response.json())

    async def get_pack_formula_analytics(
        self,
        pack_id: int,
        query: PackFormulaAnalyticsQuery | None = None,
        *,
        api_key: str,
    ) -> PackFormulaAnalyticsListResponse:
        response = await self.http.get(
            self.url(f"/analytics/packs/{pack_id}/formulas"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PackFormulaAnalyticsListResponse, response.json())

    async def get_analytics_updated(self, *, api_key: str) -> AnalyticsUpdatedResponse:
        response = await self.http.get(
            self.url("/analytics/updated"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(AnalyticsUpdatedResponse, response.json())
