from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.http_errors import raise_coda_http_error
from coda_mcp.models.workspaces import WorkspaceItem, WorkspacesListResponse
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class WorkspacesClient(CodaRequestMixin):
    """Workspaces (Coda API "Workspaces")."""

    http: httpx.AsyncClient
    base_url: str

    async def list_workspaces(self, *, api_key: str) -> WorkspacesListResponse:
        response = await self.http.get(
            self.url("/workspaces"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(WorkspacesListResponse, response.json())

    async def get_workspace(self, workspace_id: str, *, api_key: str) -> WorkspaceItem:
        w = quote(workspace_id, safe="")
        response = await self.http.get(
            self.url(f"/workspaces/{w}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(WorkspaceItem, response.json())
