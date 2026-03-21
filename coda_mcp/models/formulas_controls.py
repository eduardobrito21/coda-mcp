from pydantic import BaseModel, ConfigDict, Field, HttpUrl, JsonValue

from .common import ListEnvelope


class PageReference(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "page"
    href: str | None = None
    browser_link: HttpUrl | None = Field(None, alias="browserLink")
    name: str | None = None


class FormulasListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    limit: int | None = None
    page_token: str | None = Field(None, alias="pageToken")
    sort_by: str | None = Field(None, alias="sortBy")


class FormulaListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "formula"
    href: str | None = None
    name: str
    parent: PageReference | None = None


class FormulasListResponse(ListEnvelope):
    items: list[FormulaListItem]


class FormulaDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "formula"
    href: str | None = None
    name: str
    value: JsonValue
    parent: PageReference | None = None


class ControlsListQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    limit: int | None = None
    page_token: str | None = Field(None, alias="pageToken")
    sort_by: str | None = Field(None, alias="sortBy")


class ControlListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "control"
    href: str | None = None
    name: str
    parent: PageReference | None = None


class ControlsListResponse(ListEnvelope):
    items: list[ControlListItem]


class ControlDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "control"
    href: str | None = None
    name: str
    control_type: str = Field(alias="controlType")
    value: JsonValue
    parent: PageReference | None = None
