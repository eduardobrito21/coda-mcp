from fastmcp import FastMCP

from coda_mcp.client import coda_client
from coda_mcp.models import CreateDocBody, CreatePageBody, DocDetail


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def create_doc(
        title: str,
        source_doc_id: str = "",
        folder_id: str = "",
    ) -> DocDetail:
        """Create a new Coda doc. Optionally copy from an existing doc (source_doc_id) or place it in a specific folder (folder_id)."""
        payload: dict[str, object] = {"title": title}
        if source_doc_id:
            payload["sourceDoc"] = source_doc_id
        if folder_id:
            payload["folderId"] = folder_id
        body = CreateDocBody.model_validate(payload)
        return await coda_client.docs.create_doc(body)

    @mcp.tool()
    async def create_page(
        doc_id: str,
        name: str,
        content: str = "",
        parent_page_id: str = "",
    ) -> str:
        """Create a new page in a Coda doc. Optionally provide markdown content and a parent_page_id to nest it as a subpage."""
        payload: dict[str, object] = {"name": name}
        if parent_page_id:
            payload["parentPageId"] = parent_page_id
        if content:
            payload["pageContent"] = {
                "type": "canvas",
                "canvasContent": {"format": "markdown", "content": content},
            }
        body = CreatePageBody.model_validate(payload)
        result = await coda_client.doc_structure.create_page(doc_id, body)
        return f"Page '{name}' created (request_id={result.request_id}, page_id={result.id})."
