from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.http_errors import raise_coda_http_error
from coda_mcp.models import (
    AclMetadataResponse,
    AclSettingsResponse,
    AddPermissionBody,
    AddPermissionResult,
    CreateDocBody,
    DeletePermissionResult,
    DocCategoriesResponse,
    DocDeleteResult,
    DocDetail,
    DocsListQuery,
    DocsListResponse,
    DocUpdateResult,
    PatchAclSettingsBody,
    PatchDocBody,
    PermissionsListQuery,
    PermissionsListResponse,
    PrincipalsSearchQuery,
    PrincipalsSearchResponse,
    PublishDocBody,
    PublishQueuedResponse,
    UnpublishResult,
)
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class DocsClient(CodaRequestMixin):
    """Docs CRUD, permissions, and publishing ([Coda API — Docs](https://coda.io/developers/apis/v1#tag/Docs))."""

    http: httpx.AsyncClient
    base_url: str

    def _doc(self, doc_id: str, suffix: str = "") -> str:
        return self.url(f"/docs/{quote(doc_id, safe='')}{suffix}")

    async def list_docs(
        self, query: DocsListQuery | None = None, *, api_key: str
    ) -> DocsListResponse:
        response = await self.http.get(
            self.url("/docs"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DocsListResponse, response.json())

    async def create_doc(self, body: CreateDocBody, *, api_key: str) -> DocDetail:
        response = await self.http.post(
            self.url("/docs"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DocDetail, response.json())

    async def get_doc(self, doc_id: str, *, api_key: str) -> DocDetail:
        response = await self.http.get(
            self._doc(doc_id),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DocDetail, response.json())

    async def patch_doc(self, doc_id: str, body: PatchDocBody, *, api_key: str) -> DocUpdateResult:
        response = await self.http.patch(
            self._doc(doc_id),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DocUpdateResult, response.json())

    async def delete_doc(self, doc_id: str, *, api_key: str) -> DocDeleteResult:
        response = await self.http.delete(
            self._doc(doc_id),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DocDeleteResult, response.json())

    async def get_acl_metadata(self, doc_id: str, *, api_key: str) -> AclMetadataResponse:
        response = await self.http.get(
            self._doc(doc_id, "/acl/metadata"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(AclMetadataResponse, response.json())

    async def list_permissions(
        self,
        doc_id: str,
        query: PermissionsListQuery | None = None,
        *,
        api_key: str,
    ) -> PermissionsListResponse:
        response = await self.http.get(
            self._doc(doc_id, "/acl/permissions"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PermissionsListResponse, response.json())

    async def add_permission(
        self, doc_id: str, body: AddPermissionBody, *, api_key: str
    ) -> AddPermissionResult:
        response = await self.http.post(
            self._doc(doc_id, "/acl/permissions"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(AddPermissionResult, response.json())

    async def delete_permission(
        self, doc_id: str, permission_id: str, *, api_key: str
    ) -> DeletePermissionResult:
        response = await self.http.delete(
            self._doc(doc_id, f"/acl/permissions/{quote(permission_id, safe='')}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DeletePermissionResult, response.json())

    async def search_principals(
        self,
        doc_id: str,
        query: PrincipalsSearchQuery | None = None,
        *,
        api_key: str,
    ) -> PrincipalsSearchResponse:
        response = await self.http.get(
            self._doc(doc_id, "/acl/principals/search"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PrincipalsSearchResponse, response.json())

    async def get_acl_settings(self, doc_id: str, *, api_key: str) -> AclSettingsResponse:
        response = await self.http.get(
            self._doc(doc_id, "/acl/settings"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(AclSettingsResponse, response.json())

    async def patch_acl_settings(
        self,
        doc_id: str,
        body: PatchAclSettingsBody,
        *,
        api_key: str,
    ) -> AclSettingsResponse:
        response = await self.http.patch(
            self._doc(doc_id, "/acl/settings"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(AclSettingsResponse, response.json())

    async def list_doc_categories(self, *, api_key: str) -> DocCategoriesResponse:
        response = await self.http.get(
            self.url("/categories"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(DocCategoriesResponse, response.json())

    async def publish_doc(
        self, doc_id: str, body: PublishDocBody, *, api_key: str
    ) -> PublishQueuedResponse:
        response = await self.http.put(
            self._doc(doc_id, "/publish"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PublishQueuedResponse, response.json())

    async def unpublish_doc(self, doc_id: str, *, api_key: str) -> UnpublishResult:
        response = await self.http.delete(
            self._doc(doc_id, "/publish"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(UnpublishResult, response.json())
