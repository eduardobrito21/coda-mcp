from pydantic import BaseModel, ConfigDict, Field, JsonValue


class TriggerAutomationBody(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    payload: dict[str, JsonValue] | None = None


class TriggerAutomationResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    request_id: str = Field(alias="requestId")
