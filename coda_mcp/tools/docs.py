from fastmcp import FastMCP

from coda_mcp.client import coda_client
from coda_mcp.dependencies import CodaApiKeyDependency
from coda_mcp.models import (
    CodaDoc,
    DocCategoriesResponse,
    DocDetail,
    DocsListQuery,
    PublishDocBody,
    PublishQueuedResponse,
    UnpublishResult,
)


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def get_doc(doc_id: str, coda_api_key: str = CodaApiKeyDependency) -> DocDetail:
        """Return full metadata for a Coda doc (owner, workspace, folder, published state, etc.)."""
        return await coda_client.docs.get_doc(doc_id, api_key=coda_api_key)

    @mcp.tool()
    async def list_doc_categories(
        coda_api_key: str = CodaApiKeyDependency,
    ) -> DocCategoriesResponse:
        """List category names available when publishing a doc to the gallery (Coda publish API)."""
        return await coda_client.docs.list_doc_categories(api_key=coda_api_key)

    @mcp.tool()
    async def publish_doc(
        doc_id: str,
        slug: str = "",
        discoverable: bool | None = None,
        earn_credit: bool | None = None,
        category_names: str = "",
        mode: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PublishQueuedResponse:
        """Queue publishing a doc (slug, gallery categories, etc.). Requires doc publish permissions; see Coda API docs."""
        payload: dict[str, object] = {}
        if slug:
            payload["slug"] = slug
        if discoverable is not None:
            payload["discoverable"] = discoverable
        if earn_credit is not None:
            payload["earnCredit"] = earn_credit
        if category_names.strip():
            payload["categoryNames"] = [x.strip() for x in category_names.split(",") if x.strip()]
        if mode:
            payload["mode"] = mode
        body = PublishDocBody.model_validate(payload)
        return await coda_client.docs.publish_doc(doc_id, body, api_key=coda_api_key)

    @mcp.tool()
    async def unpublish_doc(doc_id: str, coda_api_key: str = CodaApiKeyDependency) -> UnpublishResult:
        """Remove a doc from the published gallery / unpublish."""
        return await coda_client.docs.unpublish_doc(doc_id, api_key=coda_api_key)

    @mcp.tool()
    async def list_docs(query: str = "", coda_api_key: str = CodaApiKeyDependency) -> list[CodaDoc]:
        """List all Coda docs accessible with your API key. Optionally filter by name."""
        params = DocsListQuery.model_validate({"query": query}) if query else None
        data = await coda_client.docs.list_docs(params, api_key=coda_api_key)
        return [
            CodaDoc.model_validate(
                {
                    "id": item.id,
                    "name": item.name,
                    "browserLink": str(item.browser_link),
                },
            )
            for item in data.items
        ]

    @mcp.tool()
    async def search_docs(query: str, coda_api_key: str = CodaApiKeyDependency) -> list[CodaDoc]:
        """Search for Coda docs by name or keyword."""
        data = await coda_client.docs.list_docs(
            DocsListQuery.model_validate({"query": query}),
            api_key=coda_api_key,
        )
        return [
            CodaDoc.model_validate(
                {
                    "id": item.id,
                    "name": item.name,
                    "browserLink": str(item.browser_link),
                },
            )
            for item in data.items
        ]
