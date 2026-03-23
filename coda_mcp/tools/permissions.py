from fastmcp import FastMCP

from coda_mcp.client import coda_client
from coda_mcp.dependencies import CodaApiKeyDependency
from coda_mcp.models import (
    AclMetadataResponse,
    AclSettingsResponse,
    AddPermissionBody,
    AddPermissionResult,
    DeletePermissionResult,
    PatchAclSettingsBody,
    PermissionsListQuery,
    PermissionsListResponse,
    PrincipalsSearchQuery,
    PrincipalsSearchResponse,
)


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def get_sharing_metadata(
        doc_id: str, coda_api_key: str = CodaApiKeyDependency
    ) -> AclMetadataResponse:
        """Return whether the current user can share the doc and with whom (workspace/org)."""
        return await coda_client.docs.get_acl_metadata(doc_id, api_key=coda_api_key)

    @mcp.tool()
    async def list_doc_permissions(
        doc_id: str,
        limit: int | None = None,
        page_token: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PermissionsListResponse:
        """List principals and access levels for a doc."""
        q = None
        if limit is not None or page_token:
            q = PermissionsListQuery.model_validate(
                {"limit": limit, "pageToken": page_token or None},
            )
        return await coda_client.docs.list_permissions(doc_id, q, api_key=coda_api_key)

    @mcp.tool()
    async def add_doc_permission(
        doc_id: str,
        access: str,
        principal_type: str,
        principal_email: str = "",
        suppress_email: bool | None = None,
        coda_api_key: str = CodaApiKeyDependency,
    ) -> AddPermissionResult:
        """Grant access to a user or group on a doc. principal_type is e.g. user or group; set principal_email for users."""
        body = AddPermissionBody.model_validate(
            {
                "access": access,
                "principal": {"type": principal_type, "email": principal_email or None},
                "suppressEmail": suppress_email,
            },
        )
        return await coda_client.docs.add_permission(doc_id, body, api_key=coda_api_key)

    @mcp.tool()
    async def delete_doc_permission(
        doc_id: str, permission_id: str, coda_api_key: str = CodaApiKeyDependency
    ) -> DeletePermissionResult:
        """Revoke a permission entry from a doc (use list_doc_permissions for permission IDs)."""
        return await coda_client.docs.delete_permission(
            doc_id, permission_id, api_key=coda_api_key
        )

    @mcp.tool()
    async def search_doc_principals(
        doc_id: str,
        query: str = "",
        coda_api_key: str = CodaApiKeyDependency,
    ) -> PrincipalsSearchResponse:
        """Search users and workspace groups that can be granted access on a doc."""
        q = PrincipalsSearchQuery.model_validate({"query": query or None})
        return await coda_client.docs.search_principals(doc_id, q, api_key=coda_api_key)

    @mcp.tool()
    async def get_acl_settings(
        doc_id: str, coda_api_key: str = CodaApiKeyDependency
    ) -> AclSettingsResponse:
        """Get doc-level sharing settings (copying, who can change permissions, etc.)."""
        return await coda_client.docs.get_acl_settings(doc_id, api_key=coda_api_key)

    @mcp.tool()
    async def update_acl_settings(
        doc_id: str,
        allow_editors_to_change_permissions: bool | None = None,
        allow_copying: bool | None = None,
        allow_viewers_to_request_editing: bool | None = None,
        coda_api_key: str = CodaApiKeyDependency,
    ) -> AclSettingsResponse:
        """Update doc-level sharing settings. Omit a field to leave it unchanged."""
        body = PatchAclSettingsBody.model_validate(
            {
                "allowEditorsToChangePermissions": allow_editors_to_change_permissions,
                "allowCopying": allow_copying,
                "allowViewersToRequestEditing": allow_viewers_to_request_editing,
            },
        )
        return await coda_client.docs.patch_acl_settings(doc_id, body, api_key=coda_api_key)
