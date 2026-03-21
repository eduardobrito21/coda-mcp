from functools import cached_property

import httpx

from coda_mcp.config import Settings, settings

from .common import CodaRequestMixin
from .doc_structure import DocStructureClient
from .docs import DocsClient
from .folders import FoldersClient
from .formulas_controls import FormulasControlsClient
from .miscellaneous import MiscellaneousClient
from .tables import TablesClient


class CodaClient(CodaRequestMixin):
    """Async HTTP client for the Coda REST API (v1), grouped by API doc sections."""

    _settings: Settings

    def __init__(self, settings: Settings):
        self._settings = settings
        self.http = httpx.AsyncClient(
            headers=self._headers(),
            timeout=httpx.Timeout(30.0),
        )
        self.base_url = settings.coda_base_url.rstrip("/") + "/"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._settings.coda_api_key.get_secret_value()}",
            "Content-Type": "application/json",
        }

    @cached_property
    def docs(self) -> DocsClient:
        return DocsClient(http=self.http, base_url=self.base_url)

    @cached_property
    def doc_structure(self) -> DocStructureClient:
        return DocStructureClient(http=self.http, base_url=self.base_url)

    @cached_property
    def folders(self) -> FoldersClient:
        return FoldersClient(http=self.http, base_url=self.base_url)

    @cached_property
    def tables(self) -> TablesClient:
        return TablesClient(http=self.http, base_url=self.base_url)

    @cached_property
    def formulas_controls(self) -> FormulasControlsClient:
        return FormulasControlsClient(http=self.http, base_url=self.base_url)

    @cached_property
    def miscellaneous(self) -> MiscellaneousClient:
        return MiscellaneousClient(http=self.http, base_url=self.base_url)

    async def aclose(self):
        await self.http.aclose()


coda_client = CodaClient(settings)
