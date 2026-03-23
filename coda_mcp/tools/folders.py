from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from coda_mcp.client import coda_client
from coda_mcp.dependencies import CodaApiKeyDependency
from coda_mcp.models import CreateFolderBody, DeleteFolderResult, FolderItem, UpdateFolderBody


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def create_folder(
        name: str,
        workspace_id: str,
        description: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> FolderItem:
        """Create a folder in a workspace."""
        body = CreateFolderBody.model_validate(
            {
                "name": name,
                "workspaceId": workspace_id,
                "description": description or None,
            },
        )
        return await coda_client.folders.create_folder(body, api_key=coda_api_key)

    @mcp.tool()
    async def get_folder(folder_id: str, coda_api_key: str = CodaApiKeyDependency) -> FolderItem:
        """Get folder metadata by ID."""
        return await coda_client.folders.get_folder(folder_id, api_key=coda_api_key)

    @mcp.tool()
    async def patch_folder(
        folder_id: str,
        name: str = "",
        description: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> FolderItem:
        """Update folder name and/or description. Pass only fields you want to change."""
        if not name and not description:
            raise ToolError("Provide at least one of name or description to update the folder.")
        body = UpdateFolderBody.model_validate(
            {"name": name or None, "description": description or None},
        )
        return await coda_client.folders.patch_folder(folder_id, body, api_key=coda_api_key)

    @mcp.tool()
    async def delete_folder(
        folder_id: str, coda_api_key: str = CodaApiKeyDependency
    ) -> DeleteFolderResult:
        """Delete a folder. Docs inside may need to be moved first depending on Coda rules."""
        return await coda_client.folders.delete_folder(folder_id, api_key=coda_api_key)
