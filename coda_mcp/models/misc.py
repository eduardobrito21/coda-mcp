from pydantic import BaseModel, ConfigDict, Field, HttpUrl, JsonValue


class WhoamiResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    name: str
    login_id: str = Field(alias="loginId")
    type: str = "user"
    scoped: bool
    token_name: str = Field(alias="tokenName")
    href: str
    picture_link: HttpUrl | None = Field(None, alias="pictureLink")
    workspace: dict[str, JsonValue] | None = None


class ResolveBrowserLinkQuery(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    url: str
    degrade_gracefully: bool | None = Field(None, alias="degradeGracefully")


class ResolvedResource(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    type: str
    id: str | None = None
    name: str | None = None
    href: str | None = None


class ResolveBrowserLinkResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    type: str
    href: str
    resource: ResolvedResource
    browser_link: HttpUrl | None = Field(None, alias="browserLink")


class MutationStatusResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    completed: bool
    warning: str | None = None
