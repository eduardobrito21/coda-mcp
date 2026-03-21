from fastmcp import FastMCP

from coda_mcp.client import coda_client
from coda_mcp.models import FolderItem, FoldersListQuery, PatchDocBody


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def delete_doc(doc_id: str) -> str:
        """Permanently delete a Coda doc by ID. This cannot be undone."""
        await coda_client.docs.delete_doc(doc_id)
        return f"Doc {doc_id} deleted successfully."

    @mcp.tool()
    async def delete_page(doc_id: str, page_id: str) -> str:
        """Permanently delete a page from a Coda doc. This cannot be undone."""
        await coda_client.doc_structure.delete_page(doc_id, page_id)
        return f"Page {page_id} deleted from doc {doc_id}. This cannot be undone."

    @mcp.tool()
    async def list_folders(workspace_id: str = "") -> list[FolderItem]:
        """List all folders in the workspace. Useful for finding folder IDs when creating docs."""
        query = (
            FoldersListQuery.model_validate({"workspaceId": workspace_id})
            if workspace_id
            else None
        )
        data = await coda_client.folders.list_folders(query)
        return data.items

    @mcp.tool()
    async def patch_doc(doc_id: str, title: str = "", icon_name: str = "") -> str:
        """Rename a Coda doc or change its icon."""
        if not title and not icon_name:
            return "Provide at least one of title or icon_name to update the doc."
        patch: dict[str, object] = {}
        if title:
            patch["title"] = title
        if icon_name:
            patch["iconName"] = icon_name
        body = PatchDocBody.model_validate(patch)
        await coda_client.docs.patch_doc(doc_id, body)
        return f"Doc {doc_id} updated successfully."
