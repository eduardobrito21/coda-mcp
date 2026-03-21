from pydantic import BaseModel, ConfigDict, Field, HttpUrl, JsonValue

from .common import ListEnvelope


class DocsListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    query: str | None = None
    is_owner: bool | None = Field(None, alias="isOwner")
    is_published: bool | None = Field(None, alias="isPublished")
    source_doc: str | None = Field(None, alias="sourceDoc")
    is_starred: bool | None = Field(None, alias="isStarred")
    in_gallery: bool | None = Field(None, alias="inGallery")
    workspace_id: str | None = Field(None, alias="workspaceId")
    folder_id: str | None = Field(None, alias="folderId")
    limit: int | None = None
    page_token: str | None = Field(None, alias="pageToken")


class DocListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "doc"
    href: str | None = None
    browser_link: HttpUrl = Field(alias="browserLink")
    name: str
    owner: str | None = None
    owner_name: str | None = Field(None, alias="ownerName")
    created_at: str | None = Field(None, alias="createdAt")
    updated_at: str | None = Field(None, alias="updatedAt")
    workspace_id: str | None = Field(None, alias="workspaceId")
    folder_id: str | None = Field(None, alias="folderId")


class DocsListResponse(ListEnvelope):
    items: list[DocListItem]


class CreateDocBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    title: str | None = None
    source_doc: str | None = Field(None, alias="sourceDoc")
    timezone: str | None = None
    folder_id: str | None = Field(None, alias="folderId")
    initial_page: dict[str, JsonValue] | None = Field(None, alias="initialPage")


class DocDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "doc"
    href: str
    browser_link: HttpUrl = Field(alias="browserLink")
    name: str
    owner: str
    owner_name: str = Field(alias="ownerName")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    workspace: dict[str, JsonValue] | None = None
    folder: dict[str, JsonValue] | None = None
    workspace_id: str | None = Field(None, alias="workspaceId")
    folder_id: str | None = Field(None, alias="folderId")
    icon: dict[str, JsonValue] | None = None
    doc_size: dict[str, JsonValue] | None = Field(None, alias="docSize")
    source_doc: dict[str, JsonValue] | None = Field(None, alias="sourceDoc")
    published: dict[str, JsonValue] | None = None
    request_id: str | None = Field(None, alias="requestId")


class PatchDocBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = None
    icon_name: str | None = Field(None, alias="iconName")


class DocDeleteResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class DocUpdateResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class AclMetadataResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    can_share: bool = Field(alias="canShare")
    can_share_with_workspace: bool = Field(alias="canShareWithWorkspace")
    can_share_with_org: bool = Field(alias="canShareWithOrg")
    can_copy: bool = Field(alias="canCopy")


class PermissionsListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    limit: int | None = None
    page_token: str | None = Field(None, alias="pageToken")


class PermissionPrincipal(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    type: str
    email: str | None = None


class PermissionItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    access: str
    principal: PermissionPrincipal


class PermissionsListResponse(ListEnvelope):
    items: list[PermissionItem]


class AddedPrincipal(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    type: str
    email: str | None = None


class AddPermissionBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    access: str
    principal: AddedPrincipal
    suppress_email: bool | None = Field(None, alias="suppressEmail")


class AddPermissionResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class DeletePermissionResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class PrincipalsSearchQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    query: str | None = None


class UserSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str | None = None
    login_id: str | None = Field(None, alias="loginId")
    type: str | None = None
    picture_link: HttpUrl | None = Field(None, alias="pictureLink")


class GroupPrincipal(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    type: str = "group"
    group_id: str = Field(alias="groupId")
    group_name: str = Field(alias="groupName")


class PrincipalsSearchResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    users: list[UserSummary]
    groups: list[GroupPrincipal]


class AclSettingsResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    allow_editors_to_change_permissions: bool = Field(alias="allowEditorsToChangePermissions")
    allow_copying: bool = Field(alias="allowCopying")
    allow_viewers_to_request_editing: bool = Field(alias="allowViewersToRequestEditing")


class PatchAclSettingsBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    allow_editors_to_change_permissions: bool | None = Field(
        None, alias="allowEditorsToChangePermissions"
    )
    allow_copying: bool | None = Field(None, alias="allowCopying")
    allow_viewers_to_request_editing: bool | None = Field(
        None, alias="allowViewersToRequestEditing"
    )


class DocCategoryItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str


class DocCategoriesResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    items: list[DocCategoryItem]


class PublishDocBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    slug: str | None = None
    discoverable: bool | None = None
    earn_credit: bool | None = Field(None, alias="earnCredit")
    category_names: list[str] | None = Field(None, alias="categoryNames")
    mode: str | None = None


class PublishQueuedResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    request_id: str = Field(alias="requestId")


class UnpublishResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
