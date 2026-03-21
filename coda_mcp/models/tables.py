from pydantic import BaseModel, ConfigDict, Field, HttpUrl, JsonValue

from .common import ListEnvelope


class TableListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "table"
    name: str
    table_type: str | None = Field(None, alias="tableType")
    row_count: int | None = Field(None, alias="rowCount")
    href: str | None = None
    browser_link: HttpUrl | None = Field(None, alias="browserLink")


class TablesListResponse(ListEnvelope):
    items: list[TableListItem]


class ColumnListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "column"
    name: str
    href: str | None = None
    calculated: bool | None = None
    format: dict[str, JsonValue] | None = None
    display: bool | None = None


class ColumnsListResponse(ListEnvelope):
    items: list[ColumnListItem]


class TableRowsQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    limit: int | None = 25
    query: str | None = None
    sort_by: str | None = Field(None, alias="sortBy")
    value_format: str | None = Field("simpleWithArrays", alias="valueFormat")
    page_token: str | None = Field(None, alias="pageToken")
    sync_token: str | None = Field(None, alias="syncToken")
    visible_only: bool | None = Field(None, alias="visibleOnly")
    use_column_names: bool | None = Field(None, alias="useColumnNames")


class RowListItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str
    type: str = "row"
    name: str | None = None
    index: int | None = None
    href: str | None = None
    browser_link: HttpUrl | None = Field(None, alias="browserLink")
    created_at: str | None = Field(None, alias="createdAt")
    updated_at: str | None = Field(None, alias="updatedAt")
    values: dict[str, JsonValue] = Field(default_factory=dict)


class RowsListResponse(ListEnvelope):
    items: list[RowListItem]
    next_sync_token: str | None = Field(None, alias="nextSyncToken")


class RowCellEdit(BaseModel):
    column: str
    value: JsonValue


class RowEdit(BaseModel):
    cells: list[RowCellEdit]


class RowsUpsertQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    disable_parsing: bool | None = Field(None, alias="disableParsing")


class RowsUpsertBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    rows: list[RowEdit]
    key_columns: list[str] = Field(default_factory=list, alias="keyColumns")


class RowsUpsertQueuedResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    request_id: str = Field(alias="requestId")
    added_row_ids: list[str] | None = Field(None, alias="addedRowIds")


class RowDeleteQueuedResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    request_id: str = Field(alias="requestId")
    id: str
