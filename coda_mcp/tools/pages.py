from fastmcp import FastMCP

from coda_mcp.client import coda_client
from coda_mcp.dependencies import CodaApiKeyDependency
from coda_mcp.models import (
    CodaPage,
    PageContentDeleteBody,
    PageContentDeleteResult,
    PageContentList,
    PageContentListQuery,
    PageDetail,
    PutPageBody,
)


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def list_pages(doc_id: str, coda_api_key: str = CodaApiKeyDependency) -> list[CodaPage]:
        """List all pages in a Coda doc."""
        data = await coda_client.doc_structure.get_pages_list(doc_id, api_key=coda_api_key)
        return [CodaPage(id=item.id, name=item.name) for item in data.items]

    @mcp.tool()
    async def get_page_metadata(
        doc_id: str, page_id: str, coda_api_key: str = CodaApiKeyDependency
    ) -> PageDetail:
        """Get page metadata from the Coda API (name, hierarchy, visibility, content type). Not the page body text."""
        return await coda_client.doc_structure.get_page_detail(doc_id, page_id, api_key=coda_api_key)

    @mcp.tool()
    async def list_page_content(
        doc_id: str,
        page_id: str,
        limit: int | None = None,
        page_token: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PageContentList:
        """List canvas content elements on a page (lines, etc.). Pagination via limit and page_token."""
        q = None
        if limit is not None or page_token:
            q = PageContentListQuery.model_validate(
                {"limit": limit, "pageToken": page_token or None, "contentFormat": "plainText"},
            )
        return await coda_client.doc_structure.list_page_content(
            doc_id, page_id, q, api_key=coda_api_key
        )

    @mcp.tool()
    async def delete_page_content(
        doc_id: str,
        page_id: str,
        element_ids: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PageContentDeleteResult:
        """Delete content on a page. Omit element_ids (or pass empty) to remove all content; otherwise comma-separated element IDs."""
        body = None
        if element_ids.strip():
            body = PageContentDeleteBody.model_validate(
                {"elementIds": [x.strip() for x in element_ids.split(",") if x.strip()]},
            )
        return await coda_client.doc_structure.delete_page_content(
            doc_id, page_id, body, api_key=coda_api_key
        )

    @mcp.tool()
    async def export_page_markdown(
        doc_id: str, page_id: str, coda_api_key: str = CodaApiKeyDependency
    ) -> str:
        """Export a page as markdown (async export job + download). For API page metadata, use get_page_metadata."""
        return await coda_client.doc_structure.export_page_markdown(
            doc_id, page_id, api_key=coda_api_key
        )

    @mcp.tool()
    async def update_page(
        doc_id: str, page_id: str, content: str, coda_api_key: str = CodaApiKeyDependency
    ) -> str:
        """Replace the full content of a Coda page."""
        body = PutPageBody.model_validate(
            {
                "contentUpdate": {
                    "insertionMode": "replace",
                    "canvasContent": {"format": "markdown", "content": content},
                },
            },
        )
        result = await coda_client.doc_structure.put_page(
            doc_id, page_id, body, api_key=coda_api_key
        )
        return f"Page update queued (request_id={result.request_id}, page_id={result.id})."
