import asyncio
from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.http_errors import raise_coda_http_error
from coda_mcp.models import (
    CreatePageBody,
    PageContentDeleteBody,
    PageContentDeleteResult,
    PageContentList,
    PageContentListQuery,
    PageDetail,
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

    async def get_page_detail(
        self,
        doc_id: str,
        page_id_or_name: str,
        *,
        api_key: str,
    ) -> PageDetail:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id_or_name)
        response = await self.http.get(
            self.url(f"/docs/{d}/pages/{p}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PageDetail, response.json())

    async def list_page_content(
        self,
        doc_id: str,
        page_id_or_name: str,
        query: PageContentListQuery | None = None,
        *,
        api_key: str,
    ) -> PageContentList:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id_or_name)
        response = await self.http.get(
            self.url(f"/docs/{d}/pages/{p}/content"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PageContentList, response.json())

    async def delete_page_content(
        self,
        doc_id: str,
        page_id_or_name: str,
        body: PageContentDeleteBody | None = None,
        *,
        api_key: str,
    ) -> PageContentDeleteResult:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id_or_name)
        url = self.url(f"/docs/{d}/pages/{p}/content")
        headers = self._auth_headers(api_key)
        if body is None:
            response = await self.http.delete(url, headers=headers)
        else:
            response = await self.http.request(
                "DELETE",
                url,
                json=body.model_dump(by_alias=True, exclude_none=True),
                headers=headers,
            )
        raise_coda_http_error(response)
        return validate_pydantic(PageContentDeleteResult, response.json())

    async def get_pages_list(
        self,
        doc_id: str,
        query: PagesListQuery | None = None,
        *,
        api_key: str,
    ) -> PagesListResponse:
        d = quote(doc_id, safe="")
        response = await self.http.get(
            self.url(f"/docs/{d}/pages"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PagesListResponse, response.json())

    async def create_page(
        self,
        doc_id: str,
        body: CreatePageBody,
        *,
        api_key: str,
    ) -> PageMutationQueuedResponse:
        d = quote(doc_id, safe="")
        response = await self.http.post(
            self.url(f"/docs/{d}/pages"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PageMutationQueuedResponse, response.json())

    async def delete_page(self, doc_id: str, page_id: str, *, api_key: str) -> None:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id)
        response = await self.http.delete(
            self.url(f"/docs/{d}/pages/{p}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)

    async def begin_page_export(
        self,
        doc_id: str,
        page_id: str,
        body: PageExportRequest,
        *,
        api_key: str,
    ) -> PageExportBeginResponse:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id)
        response = await self.http.post(
            self.url(f"/docs/{d}/pages/{p}/export"),
            json=body.model_dump(by_alias=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PageExportBeginResponse, response.json())

    async def get_page_export_status(
        self,
        doc_id: str,
        page_id: str,
        request_id: str,
        *,
        api_key: str,
    ) -> PageExportStatusResponse:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id)
        r = quote(request_id, safe="")
        response = await self.http.get(
            self.url(f"/docs/{d}/pages/{p}/export/{r}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PageExportStatusResponse, response.json())

    async def export_page_markdown(self, doc_id: str, page_id: str, *, api_key: str) -> str:
        """POST begin export, poll status, then download markdown from ``downloadLink``."""
        begin = await self.begin_page_export(
            doc_id,
            page_id,
            validate_pydantic(
                PageExportRequest,
                {"outputFormat": "markdown"},
                by_alias=True,
            ),
            api_key=api_key,
        )
        export_id = begin.id
        delay_s = 0.5
        max_attempts = 120
        download_link: str | None = None
        for _ in range(max_attempts):
            status = await self.get_page_export_status(doc_id, page_id, export_id, api_key=api_key)
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
        dl = await self.http.get(download_link, headers=self._auth_headers(api_key))
        raise_coda_http_error(dl)
        return dl.text

    async def put_page(
        self,
        doc_id: str,
        page_id: str,
        body: PutPageBody,
        *,
        api_key: str,
    ) -> PageMutationQueuedResponse:
        d = quote(doc_id, safe="")
        p = self._page_seg(page_id)
        response = await self.http.put(
            self.url(f"/docs/{d}/pages/{p}"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PageMutationQueuedResponse, response.json())
