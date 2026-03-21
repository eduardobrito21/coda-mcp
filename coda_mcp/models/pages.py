from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .common import ListEnvelope

# --- Page update (OpenAPI: PageUpdate / PageContentUpdate / PageContent) ---


class PageContent(BaseModel):
    """Canvas content block (``PageContent`` in the OpenAPI spec)."""

    model_config = ConfigDict(populate_by_name=True)

    format: Literal["html", "markdown"]
    content: str


class PageContentUpdate(BaseModel):
    """``contentUpdate`` on ``PageUpdate``."""

    model_config = ConfigDict(populate_by_name=True)

    insertion_mode: Literal["append", "prepend", "replace"] = Field(alias="insertionMode")
    element_id: str | None = Field(None, alias="elementId")
    canvas_content: PageContent = Field(alias="canvasContent")


class PagesListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    limit: int | None = None
    page_token: str | None = Field(None, alias="pageToken")


class PageListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "page"
    name: str
    href: str | None = None
    browser_link: HttpUrl | None = Field(None, alias="browserLink")
    content_type: str | None = Field(None, alias="contentType")
    subtitle: str | None = None


class PagesListResponse(ListEnvelope):
    items: list[PageListItem]


class PageExportRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    output_format: Literal["html", "markdown"] = Field(alias="outputFormat")


class PageExportBeginResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    status: str
    href: str


class PageExportStatusResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    status: str
    href: str
    download_link: str | None = Field(None, alias="downloadLink")
    error: str | None = None


class PutPageBody(BaseModel):
    """Body for PUT ``/docs/{docId}/pages/{pageIdOrName}`` (OpenAPI: ``PageUpdate``)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    name: str | None = None
    subtitle: str | None = None
    icon_name: str | None = Field(None, alias="iconName")
    image_url: str | None = Field(None, alias="imageUrl")
    is_hidden: bool | None = Field(None, alias="isHidden")
    content_update: PageContentUpdate | None = Field(None, alias="contentUpdate")


class PageMutationQueuedResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    request_id: str = Field(alias="requestId")
    id: str
