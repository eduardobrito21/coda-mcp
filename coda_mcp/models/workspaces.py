from pydantic import BaseModel, ConfigDict, Field

from .common import ListEnvelope


class WorkspaceItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "workspace"
    organization_id: str | None = Field(None, alias="organizationId")
    name: str
    description: str | None = None


class WorkspacesListResponse(ListEnvelope):
    items: list[WorkspaceItem]
