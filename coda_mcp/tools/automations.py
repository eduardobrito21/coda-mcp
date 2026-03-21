from fastmcp import FastMCP
from pydantic import JsonValue

from coda_mcp.client import coda_client
from coda_mcp.models.automations import TriggerAutomationBody, TriggerAutomationResponse


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def trigger_automation(
        doc_id: str,
        automation_id: str,
        payload: dict[str, JsonValue] | None = None,
    ) -> TriggerAutomationResponse:
        """Trigger a Coda automation to run. Optionally pass a payload dict that the automation can read.
        Use list_pages to browse a doc and find automation IDs, or ask the user to paste the automation URL."""
        body = TriggerAutomationBody(payload=payload)
        return await coda_client.automations.trigger_automation(doc_id, automation_id, body)
