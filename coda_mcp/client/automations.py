from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.http_errors import raise_coda_http_error
from coda_mcp.models.automations import TriggerAutomationBody, TriggerAutomationResponse
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class AutomationsClient(CodaRequestMixin):
    """Automations in a doc (Coda API "Automations")."""

    http: httpx.AsyncClient
    base_url: str

    async def trigger_automation(
        self,
        doc_id: str,
        automation_id: str,
        body: TriggerAutomationBody,
        *,
        api_key: str,
    ) -> TriggerAutomationResponse:
        d = quote(doc_id, safe="")
        a = quote(automation_id, safe="")
        json_body = body.model_dump(by_alias=True, exclude_none=True)
        response = await self.http.post(
            self.url(f"/docs/{d}/automations/{a}/runs"),
            json=json_body,
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(TriggerAutomationResponse, response.json())
