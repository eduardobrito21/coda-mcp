from dataclasses import dataclass
from urllib.parse import quote

import httpx

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

    async def list_folders(self, query: FoldersListQuery | None = None) -> FoldersListResponse:
        response = await self.http.get(
            self.url("/folders"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(FoldersListResponse, response.json())

    async def create_folder(self, body: CreateFolderBody) -> FolderItem:
        response = await self.http.post(
            self.url("/folders"),
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        response.raise_for_status()
        return validate_pydantic(FolderItem, response.json())

    async def get_folder(self, folder_id: str) -> FolderItem:
        response = await self.http.get(
            self.url(f"/folders/{quote(folder_id, safe='')}"),
        )
        response.raise_for_status()
        return validate_pydantic(FolderItem, response.json())

    async def patch_folder(self, folder_id: str, body: UpdateFolderBody) -> FolderItem:
        response = await self.http.patch(
            self.url(f"/folders/{quote(folder_id, safe='')}"),
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        response.raise_for_status()
        return validate_pydantic(FolderItem, response.json())

    async def delete_folder(self, folder_id: str) -> DeleteFolderResult:
        response = await self.http.delete(
            self.url(f"/folders/{quote(folder_id, safe='')}"),
        )
        response.raise_for_status()
        return validate_pydantic(DeleteFolderResult, response.json())
