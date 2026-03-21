from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.models.workspaces import WorkspaceItem, WorkspacesListResponse
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class WorkspacesClient(CodaRequestMixin):
    """Workspaces (Coda API "Workspaces")."""

    http: httpx.AsyncClient
    base_url: str

    async def list_workspaces(self) -> WorkspacesListResponse:
        response = await self.http.get(self.url("/workspaces"))
        response.raise_for_status()
        return validate_pydantic(WorkspacesListResponse, response.json())

    async def get_workspace(self, workspace_id: str) -> WorkspaceItem:
        w = quote(workspace_id, safe="")
        response = await self.http.get(self.url(f"/workspaces/{w}"))
        response.raise_for_status()
        return validate_pydantic(WorkspaceItem, response.json())
