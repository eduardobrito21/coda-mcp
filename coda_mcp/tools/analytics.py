from fastmcp import FastMCP

from coda_mcp.client import coda_client
from coda_mcp.dependencies import CodaApiKeyDependency
from coda_mcp.models import (
    AnalyticsUpdatedResponse,
    DocAnalyticsListQuery,
    DocAnalyticsListResponse,
    DocAnalyticsSummaryQuery,
    DocAnalyticsSummaryResponse,
    PackAnalyticsListQuery,
    PackAnalyticsListResponse,
    PackAnalyticsSummaryQuery,
    PackAnalyticsSummaryResponse,
    PackFormulaAnalyticsListResponse,
    PackFormulaAnalyticsQuery,
    PageAnalyticsListQuery,
    PageAnalyticsListResponse,
)


def _doc_analytics_query(
    *,
    limit: int | None,
    page_token: str,
    workspace_id: str,
    query: str,
    doc_ids: str,
    is_published: bool | None,
    since_date: str,
    until_date: str,
) -> DocAnalyticsListQuery | None:
    if not any(
        [
            limit is not None,
            page_token,
            workspace_id,
            query,
            doc_ids,
            is_published is not None,
            since_date,
            until_date,
        ],
    ):
        return None
    payload: dict[str, object] = {}
    if limit is not None:
        payload["limit"] = limit
    if page_token:
        payload["pageToken"] = page_token
    if workspace_id:
        payload["workspaceId"] = workspace_id
    if query:
        payload["query"] = query
    if doc_ids.strip():
        payload["docIds"] = [x.strip() for x in doc_ids.split(",") if x.strip()]
    if is_published is not None:
        payload["isPublished"] = is_published
    if since_date:
        payload["sinceDate"] = since_date
    if until_date:
        payload["untilDate"] = until_date
    return DocAnalyticsListQuery.model_validate(payload)


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def list_doc_analytics(
        limit: int | None = None,
        page_token: str = "",
        workspace_id: str = "",
        query: str = "",
        doc_ids: str = "",
        is_published: bool | None = None,
        since_date: str = "",
        until_date: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> DocAnalyticsListResponse:
        """List per-doc analytics (sessions, etc.). Requires analytics API access on your Coda plan."""
        q = _doc_analytics_query(
            limit=limit,
            page_token=page_token,
            workspace_id=workspace_id,
            query=query,
            doc_ids=doc_ids,
            is_published=is_published,
            since_date=since_date,
            until_date=until_date,
        )
        return await coda_client.miscellaneous.get_doc_analytics(q, api_key=coda_api_key)

    @mcp.tool()
    async def list_page_analytics(
        doc_id: str,
        limit: int | None = None,
        page_token: str = "",
        since_date: str = "",
        until_date: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PageAnalyticsListResponse:
        """List per-page analytics for a doc."""
        q = None
        if any([limit is not None, page_token, since_date, until_date]):
            q = PageAnalyticsListQuery.model_validate(
                {
                    "limit": limit,
                    "pageToken": page_token or None,
                    "sinceDate": since_date or None,
                    "untilDate": until_date or None,
                },
            )
        return await coda_client.miscellaneous.get_page_analytics(doc_id, q, api_key=coda_api_key)

    @mcp.tool()
    async def get_doc_analytics_summary(
        is_published: bool | None = None,
        since_date: str = "",
        until_date: str = "",
        workspace_id: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> DocAnalyticsSummaryResponse:
        """Aggregated doc analytics summary for the workspace scope allowed by the token."""
        q = None
        if any([is_published is not None, since_date, until_date, workspace_id]):
            q = DocAnalyticsSummaryQuery.model_validate(
                {
                    "isPublished": is_published,
                    "sinceDate": since_date or None,
                    "untilDate": until_date or None,
                    "workspaceId": workspace_id or None,
                },
            )
        return await coda_client.miscellaneous.get_doc_analytics_summary(q, api_key=coda_api_key)

    @mcp.tool()
    async def list_pack_analytics(
        limit: int | None = None,
        page_token: str = "",
        workspace_id: str = "",
        query: str = "",
        pack_ids: str = "",
        is_published: bool | None = None,
        since_date: str = "",
        until_date: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PackAnalyticsListResponse:
        """List Pack usage analytics."""
        q = None
        if any(
            [
                limit is not None,
                page_token,
                workspace_id,
                query,
                pack_ids,
                is_published is not None,
                since_date,
                until_date,
            ],
        ):
            payload: dict[str, object] = {}
            if limit is not None:
                payload["limit"] = limit
            if page_token:
                payload["pageToken"] = page_token
            if workspace_id:
                payload["workspaceId"] = workspace_id
            if query:
                payload["query"] = query
            if pack_ids.strip():
                payload["packIds"] = [int(x.strip()) for x in pack_ids.split(",") if x.strip()]
            if is_published is not None:
                payload["isPublished"] = is_published
            if since_date:
                payload["sinceDate"] = since_date
            if until_date:
                payload["untilDate"] = until_date
            q = PackAnalyticsListQuery.model_validate(payload)
        return await coda_client.miscellaneous.get_pack_analytics(q, api_key=coda_api_key)

    @mcp.tool()
    async def get_pack_analytics_summary(
        pack_ids: str = "",
        workspace_id: str = "",
        is_published: bool | None = None,
        since_date: str = "",
        until_date: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PackAnalyticsSummaryResponse:
        """Aggregated Pack analytics summary."""
        q = None
        if any([pack_ids, workspace_id, is_published is not None, since_date, until_date]):
            payload: dict[str, object] = {}
            if pack_ids.strip():
                payload["packIds"] = [int(x.strip()) for x in pack_ids.split(",") if x.strip()]
            if workspace_id:
                payload["workspaceId"] = workspace_id
            if is_published is not None:
                payload["isPublished"] = is_published
            if since_date:
                payload["sinceDate"] = since_date
            if until_date:
                payload["untilDate"] = until_date
            q = PackAnalyticsSummaryQuery.model_validate(payload)
        return await coda_client.miscellaneous.get_pack_analytics_summary(q, api_key=coda_api_key)

    @mcp.tool()
    async def list_pack_formula_analytics(
        pack_id: int,
        limit: int | None = None,
        page_token: str = "",
        since_date: str = "",
        until_date: str = "",
        pack_formula_names: str = "",
        pack_formula_types: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PackFormulaAnalyticsListResponse:
        """List formula-level analytics for a Pack."""
        q = None
        if any(
            [
                limit is not None,
                page_token,
                since_date,
                until_date,
                pack_formula_names,
                pack_formula_types,
            ],
        ):
            payload: dict[str, object] = {}
            if limit is not None:
                payload["limit"] = limit
            if page_token:
                payload["pageToken"] = page_token
            if since_date:
                payload["sinceDate"] = since_date
            if until_date:
                payload["untilDate"] = until_date
            if pack_formula_names.strip():
                payload["packFormulaNames"] = [
                    x.strip() for x in pack_formula_names.split(",") if x.strip()
                ]
            if pack_formula_types.strip():
                payload["packFormulaTypes"] = [
                    x.strip() for x in pack_formula_types.split(",") if x.strip()
                ]
            q = PackFormulaAnalyticsQuery.model_validate(payload)
        return await coda_client.miscellaneous.get_pack_formula_analytics(
            pack_id, q, api_key=coda_api_key
        )

    @mcp.tool()
    async def get_analytics_updated(
        coda_api_key: str = CodaApiKeyDependency,
    ) -> AnalyticsUpdatedResponse:
        """Return last-updated timestamps for analytics datasets (docs, packs, pack formulas)."""
        return await coda_client.miscellaneous.get_analytics_updated(api_key=coda_api_key)
