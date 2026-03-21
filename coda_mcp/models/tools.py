from pydantic import BaseModel, ConfigDict, Field, HttpUrl, JsonValue


class CodaDoc(BaseModel):
    id: str
    name: str
    browser_link: HttpUrl = Field(alias="browserLink")

    model_config = ConfigDict(populate_by_name=True)


class CodaPage(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(populate_by_name=True)


class CodaCell(BaseModel):
    column: str
    value: JsonValue


class CodaRow(BaseModel):
    id: str
    name: str | None = None
    values: dict[str, JsonValue] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class UpsertRowInput(BaseModel):
    doc_id: str
    table_id: str
    cells: list[CodaCell]
    key_columns: list[str] = []
