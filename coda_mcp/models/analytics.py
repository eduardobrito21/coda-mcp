from pydantic import BaseModel, ConfigDict, Field, JsonValue

from .common import ListEnvelope


class DocAnalyticsListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    doc_ids: list[str] | None = Field(None, alias="docIds")
    workspace_id: str | None = Field(None, alias="workspaceId")
    query: str | None = None
    is_published: bool | None = Field(None, alias="isPublished")
    since_date: str | None = Field(None, alias="sinceDate")
    until_date: str | None = Field(None, alias="untilDate")
    scale: str | None = None
    page_token: str | None = Field(None, alias="pageToken")
    order_by: str | None = Field(None, alias="orderBy")
    direction: str | None = None
    limit: int | None = None


class DocAnalyticsListResponse(ListEnvelope):
    items: list[dict[str, JsonValue]]


class PageAnalyticsListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    since_date: str | None = Field(None, alias="sinceDate")
    until_date: str | None = Field(None, alias="untilDate")
    page_token: str | None = Field(None, alias="pageToken")
    limit: int | None = None


class PageAnalyticsListResponse(ListEnvelope):
    items: list[dict[str, JsonValue]]


class DocAnalyticsSummaryQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    is_published: bool | None = Field(None, alias="isPublished")
    since_date: str | None = Field(None, alias="sinceDate")
    until_date: str | None = Field(None, alias="untilDate")
    workspace_id: str | None = Field(None, alias="workspaceId")


class DocAnalyticsSummaryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    total_sessions: int = Field(alias="totalSessions")


class PackAnalyticsListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pack_ids: list[int] | None = Field(None, alias="packIds")
    workspace_id: str | None = Field(None, alias="workspaceId")
    query: str | None = None
    since_date: str | None = Field(None, alias="sinceDate")
    until_date: str | None = Field(None, alias="untilDate")
    scale: str | None = None
    page_token: str | None = Field(None, alias="pageToken")
    order_by: str | None = Field(None, alias="orderBy")
    direction: str | None = None
    is_published: bool | None = Field(None, alias="isPublished")
    limit: int | None = None


class PackAnalyticsListResponse(ListEnvelope):
    items: list[dict[str, JsonValue]]


class PackAnalyticsSummaryQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pack_ids: list[int] | None = Field(None, alias="packIds")
    workspace_id: str | None = Field(None, alias="workspaceId")
    is_published: bool | None = Field(None, alias="isPublished")
    since_date: str | None = Field(None, alias="sinceDate")
    until_date: str | None = Field(None, alias="untilDate")


class PackAnalyticsSummaryResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    total_doc_installs: int = Field(alias="totalDocInstalls")
    total_workspace_installs: int = Field(alias="totalWorkspaceInstalls")
    total_invocations: int = Field(alias="totalInvocations")


class PackFormulaAnalyticsQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    pack_formula_names: list[str] | None = Field(None, alias="packFormulaNames")
    pack_formula_types: list[str] | None = Field(None, alias="packFormulaTypes")
    since_date: str | None = Field(None, alias="sinceDate")
    until_date: str | None = Field(None, alias="untilDate")
    scale: str | None = None
    page_token: str | None = Field(None, alias="pageToken")
    order_by: str | None = Field(None, alias="orderBy")
    direction: str | None = None
    limit: int | None = None


class PackFormulaAnalyticsListResponse(ListEnvelope):
    items: list[dict[str, JsonValue]]


class AnalyticsUpdatedResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    doc_analytics_last_updated: str = Field(alias="docAnalyticsLastUpdated")
    pack_analytics_last_updated: str = Field(alias="packAnalyticsLastUpdated")
    pack_formula_analytics_last_updated: str = Field(alias="packFormulaAnalyticsLastUpdated")
