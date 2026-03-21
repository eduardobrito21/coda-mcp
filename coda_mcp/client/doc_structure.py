import asyncio
from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.models import (
    CreatePageBody,
    PageExportBeginResponse,
    PageExportRequest,
    PageExportStatusResponse,
    PageMutationQueuedResponse,
    PagesListQuery,
    PagesListResponse,
    PutPageBody,
)
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class DocStructureClient(CodaRequestMixin):
    """Pages and page content inside a doc (Coda API “Doc structure”)."""

    http: httpx.AsyncClient
    base_url: str

    def _page_seg(self, page_id_or_name: str) -> str:
        return quote(page_id_or_name, safe="")

    async def get_pages_list(
        self,
        doc_id: str,
        query: PagesListQuery | None = None,
    ) -> PagesListResponse:
        d = quote(doc_id, safe="")
        response = await self.http.get(
            self.url(f"/docs/{d}/pages"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(PagesListResponse, response.json())

    async def create_page(
        self,
        doc_id: str,
        body: CreatePageBody,
    ) -> PageMutationQueuedResponse:
        d = quote(doc_id, safe="")
        response = await self.http.post(
            self.url(f"/docs/{d}/pages"),
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        response.raise_for_status()
        return validate_pydantic(PageMutationQueuedResponse, response.json())

    async def delete_page(self, doc_id: str, page_id: str) -> None:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id)
        response = await self.http.delete(self.url(f"/docs/{d}/pages/{p}"))
        response.raise_for_status()

    async def begin_page_export(
        self,
        doc_id: str,
        page_id: str,
        body: PageExportRequest,
    ) -> PageExportBeginResponse:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id)
        response = await self.http.post(
            self.url(f"/docs/{d}/pages/{p}/export"),
            json=body.model_dump(by_alias=True),
        )
        response.raise_for_status()
        return validate_pydantic(PageExportBeginResponse, response.json())

    async def get_page_export_status(
        self,
        doc_id: str,
        page_id: str,
        request_id: str,
    ) -> PageExportStatusResponse:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id)
        r = quote(request_id, safe="")
        response = await self.http.get(
            self.url(f"/docs/{d}/pages/{p}/export/{r}"),
        )
        response.raise_for_status()
        return validate_pydantic(PageExportStatusResponse, response.json())

    async def export_page_markdown(self, doc_id: str, page_id: str) -> str:
        """POST begin export, poll status, then download markdown from ``downloadLink``."""
        begin = await self.begin_page_export(
            doc_id,
            page_id,
            validate_pydantic(
                PageExportRequest,
                {"outputFormat": "markdown"},
                by_alias=True,
            ),
        )
        export_id = begin.id
        delay_s = 0.5
        max_attempts = 120
        download_link: str | None = None
        for _ in range(max_attempts):
            status = await self.get_page_export_status(doc_id, page_id, export_id)
            if status.error:
                msg = f"Coda export failed: {status.error}"
                raise RuntimeError(msg)
            if status.download_link:
                download_link = status.download_link
                break
            await asyncio.sleep(delay_s)
        if not download_link:
            msg = "Timed out waiting for page export download link"
            raise TimeoutError(msg)
        dl = await self.http.get(download_link)
        dl.raise_for_status()
        return dl.text

    async def put_page(
        self,
        doc_id: str,
        page_id: str,
        body: PutPageBody,
    ) -> PageMutationQueuedResponse:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id)
        response = await self.http.put(
            self.url(f"/docs/{d}/pages/{p}"),
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        response.raise_for_status()
        return validate_pydantic(PageMutationQueuedResponse, response.json())
