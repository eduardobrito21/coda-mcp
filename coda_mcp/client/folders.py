from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.http_errors import raise_coda_http_error
from coda_mcp.models import (
    CreateFolderBody,
    DeleteFolderResult,
    FolderItem,
    FoldersListQuery,
    FoldersListResponse,
    UpdateFolderBody,
)
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class FoldersClient(CodaRequestMixin):
    """Folders ([Coda API — Folders](https://coda.io/developers/apis/v1#tag/Folders))."""

    http: httpx.AsyncClient
    base_url: str

    async def list_folders(
        self, query: FoldersListQuery | None = None, *, api_key: str
    ) -> FoldersListResponse:
        response = await self.http.get(
            self.url("/folders"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(FoldersListResponse, response.json())

    async def create_folder(self, body: CreateFolderBody, *, api_key: str) -> FolderItem:
        response = await self.http.post(
            self.url("/folders"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(FolderItem, response.json())

    async def get_folder(self, folder_id: str, *, api_key: str) -> FolderItem:
        response = await self.http.get(
            self.url(f"/folders/{quote(folder_id, safe='')}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(FolderItem, response.json())

    async def patch_folder(
        self, folder_id: str, body: UpdateFolderBody, *, api_key: str
    ) -> FolderItem:
        response = await self.http.patch(
            self.url(f"/folders/{quote(folder_id, safe='')}"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(FolderItem, response.json())

    async def delete_folder(self, folder_id: str, *, api_key: str) -> DeleteFolderResult:
        response = await self.http.delete(
            self.url(f"/folders/{quote(folder_id, safe='')}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DeleteFolderResult, response.json())
