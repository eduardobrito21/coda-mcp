from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.http_errors import raise_coda_http_error
from coda_mcp.models import (
    ColumnListItem,
    ColumnsListResponse,
    PushButtonQueuedResponse,
    RowDeleteQueuedResponse,
    RowListItem,
    RowsDeleteBody,
    RowsDeleteQueuedResponse,
    RowsListResponse,
    RowsUpsertBody,
    RowsUpsertQuery,
    RowsUpsertQueuedResponse,
    RowUpdateBody,
    TableListItem,
    TableRowsQuery,
    TablesListResponse,
)
from coda_mcp.validation import validate_pydantic

from .common import CodaRequestMixin


@dataclass
class TablesClient(CodaRequestMixin):
    """Tables, views, columns, and rows (Coda API “Tables and views”)."""

    http: httpx.AsyncClient
    base_url: str

    def _doc(self, doc_id: str) -> str:
        return quote(doc_id, safe="")

    def _seg(self, table_or_row_id: str) -> str:
        return quote(table_or_row_id, safe="")

    async def list_tables(self, doc_id: str, *, api_key: str) -> TablesListResponse:
        d = self._doc(doc_id)
        response = await self.http.get(
            self.url(f"/docs/{d}/tables"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(TablesListResponse, response.json())

    async def list_columns(
        self, doc_id: str, table_id: str, *, api_key: str
    ) -> ColumnsListResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        response = await self.http.get(
            self.url(f"/docs/{d}/tables/{t}/columns"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(ColumnsListResponse, response.json())

    async def get_column(
        self, doc_id: str, table_id: str, column_id: str, *, api_key: str
    ) -> ColumnListItem:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        c = self._seg(column_id)
        response = await self.http.get(
            self.url(f"/docs/{d}/tables/{t}/columns/{c}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(ColumnListItem, response.json())

    async def get_table_rows(
        self,
        doc_id: str,
        table_id: str,
        query: TableRowsQuery | None = None,
        *,
        api_key: str,
    ) -> RowsListResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        response = await self.http.get(
            self.url(f"/docs/{d}/tables/{t}/rows"),
            params=self.query_dict(query),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(RowsListResponse, response.json())

    async def post_table_rows(
        self,
        doc_id: str,
        table_id: str,
        body: RowsUpsertBody,
        query: RowsUpsertQuery | None = None,
        *,
        api_key: str,
    ) -> RowsUpsertQueuedResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        response = await self.http.post(
            self.url(f"/docs/{d}/tables/{t}/rows"),
            params=self.query_dict(query),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(RowsUpsertQueuedResponse, response.json())

    async def get_table(self, doc_id: str, table_id: str, *, api_key: str) -> TableListItem:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        response = await self.http.get(
            self.url(f"/docs/{d}/tables/{t}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(TableListItem, response.json())

    async def get_row(
        self, doc_id: str, table_id: str, row_id: str, *, api_key: str
    ) -> RowListItem:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        r = self._seg(row_id)
        response = await self.http.get(
            self.url(f"/docs/{d}/tables/{t}/rows/{r}"),
            params={"valueFormat": "simpleWithArrays"},
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(RowListItem, response.json())

    async def update_row(
        self,
        doc_id: str,
        table_id: str,
        row_id: str,
        body: RowUpdateBody,
        *,
        api_key: str,
    ) -> RowDeleteQueuedResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        r = self._seg(row_id)
        response = await self.http.put(
            self.url(f"/docs/{d}/tables/{t}/rows/{r}"),
            json=body.model_dump(by_alias=True, exclude_none=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(RowDeleteQueuedResponse, response.json())

    async def delete_rows(
        self,
        doc_id: str,
        table_id: str,
        body: RowsDeleteBody,
        *,
        api_key: str,
    ) -> RowsDeleteQueuedResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        response = await self.http.request(
            "DELETE",
            self.url(f"/docs/{d}/tables/{t}/rows"),
            json=body.model_dump(by_alias=True),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(RowsDeleteQueuedResponse, response.json())

    async def delete_table_row(
        self,
        doc_id: str,
        table_id: str,
        row_id: str,
        *,
        api_key: str,
    ) -> RowDeleteQueuedResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        r = self._seg(row_id)
        response = await self.http.delete(
            self.url(f"/docs/{d}/tables/{t}/rows/{r}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(RowDeleteQueuedResponse, response.json())

    async def push_button(
        self,
        doc_id: str,
        table_id: str,
        row_id: str,
        column_id: str,
        *,
        api_key: str,
    ) -> PushButtonQueuedResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        r = self._seg(row_id)
        c = self._seg(column_id)
        response = await self.http.post(
            self.url(f"/docs/{d}/tables/{t}/rows/{r}/buttons/{c}"),
            headers=self._auth_headers(api_key),
        )
        raise_coda_http_error(response)
        return validate_pydantic(PushButtonQueuedResponse, response.json())
