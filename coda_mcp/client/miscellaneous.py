from dataclasses import dataclass
from urllib.parse import quote

import httpx

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

    async def get_whoami(self) -> WhoamiResponse:
        response = await self.http.get(self.url("/whoami"))
        response.raise_for_status()
        return validate_pydantic(WhoamiResponse, response.json())

    async def get_resolve_browser_link(
        self, query: ResolveBrowserLinkQuery
    ) -> ResolveBrowserLinkResponse:
        response = await self.http.get(
            self.url("/resolveBrowserLink"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(ResolveBrowserLinkResponse, response.json())

    async def get_mutation_status(self, request_id: str) -> MutationStatusResponse:
        response = await self.http.get(
            self.url(f"/mutationStatus/{quote(request_id, safe='')}"),
        )
        response.raise_for_status()
        return validate_pydantic(MutationStatusResponse, response.json())

    async def get_doc_analytics(
        self, query: DocAnalyticsListQuery | None = None
    ) -> DocAnalyticsListResponse:
        response = await self.http.get(
            self.url("/analytics/docs"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(DocAnalyticsListResponse, response.json())

    async def get_page_analytics(
        self,
        doc_id: str,
        query: PageAnalyticsListQuery | None = None,
    ) -> PageAnalyticsListResponse:
        response = await self.http.get(
            self.url(f"/analytics/docs/{quote(doc_id, safe='')}/pages"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(PageAnalyticsListResponse, response.json())

    async def get_doc_analytics_summary(
        self,
        query: DocAnalyticsSummaryQuery | None = None,
    ) -> DocAnalyticsSummaryResponse:
        response = await self.http.get(
            self.url("/analytics/docs/summary"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(DocAnalyticsSummaryResponse, response.json())

    async def get_pack_analytics(
        self, query: PackAnalyticsListQuery | None = None
    ) -> PackAnalyticsListResponse:
        response = await self.http.get(
            self.url("/analytics/packs"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(PackAnalyticsListResponse, response.json())

    async def get_pack_analytics_summary(
        self,
        query: PackAnalyticsSummaryQuery | None = None,
    ) -> PackAnalyticsSummaryResponse:
        response = await self.http.get(
            self.url("/analytics/packs/summary"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(PackAnalyticsSummaryResponse, response.json())

    async def get_pack_formula_analytics(
        self,
        pack_id: int,
        query: PackFormulaAnalyticsQuery | None = None,
    ) -> PackFormulaAnalyticsListResponse:
        response = await self.http.get(
            self.url(f"/analytics/packs/{pack_id}/formulas"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(PackFormulaAnalyticsListResponse, response.json())

    async def get_analytics_updated(self) -> AnalyticsUpdatedResponse:
        response = await self.http.get(self.url("/analytics/updated"))
        response.raise_for_status()
        return validate_pydantic(AnalyticsUpdatedResponse, response.json())
