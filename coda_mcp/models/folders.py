from pydantic import BaseModel, ConfigDict, Field, HttpUrl, JsonValue

from .common import ListEnvelope


class FoldersListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    workspace_id: str | None = Field(None, alias="workspaceId")
    is_starred: bool | None = Field(None, alias="isStarred")
    limit: int | None = None
    page_token: str | None = Field(None, alias="pageToken")


class FolderItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "folder"
    name: str
    browser_link: HttpUrl = Field(alias="browserLink")
    description: str | None = None
    workspace: dict[str, JsonValue] | None = None
    created_at: str | None = Field(None, alias="createdAt")
    can_edit: bool | None = Field(None, alias="canEdit")
    icon: dict[str, JsonValue] | None = None


class FoldersListResponse(ListEnvelope):
    items: list[FolderItem]


class CreateFolderBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    workspace_id: str = Field(alias="workspaceId")
    description: str | None = None


class UpdateFolderBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str | None = None
    description: str | None = None


class DeleteFolderResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
