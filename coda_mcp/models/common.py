from pydantic import BaseModel, ConfigDict, Field


class ListEnvelope(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    href: str | None = None
    next_page_token: str | None = Field(None, alias="nextPageToken")
    next_page_link: str | None = Field(None, alias="nextPageLink")
