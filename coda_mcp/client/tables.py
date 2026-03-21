from dataclasses import dataclass
from urllib.parse import quote

import httpx

from coda_mcp.models import (
    ColumnsListResponse,
    RowDeleteQueuedResponse,
    RowsListResponse,
    RowsUpsertBody,
    RowsUpsertQuery,
    RowsUpsertQueuedResponse,
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

    async def list_tables(self, doc_id: str) -> TablesListResponse:
        d = self._doc(doc_id)
        response = await self.http.get(self.url(f"/docs/{d}/tables"))
        response.raise_for_status()
        return validate_pydantic(TablesListResponse, response.json())

    async def list_columns(self, doc_id: str, table_id: str) -> ColumnsListResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        response = await self.http.get(self.url(f"/docs/{d}/tables/{t}/columns"))
        response.raise_for_status()
        return validate_pydantic(ColumnsListResponse, response.json())

    async def get_table_rows(
        self,
        doc_id: str,
        table_id: str,
        query: TableRowsQuery | None = None,
    ) -> RowsListResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        response = await self.http.get(
            self.url(f"/docs/{d}/tables/{t}/rows"),
            params=self.query_dict(query),
        )
        response.raise_for_status()
        return validate_pydantic(RowsListResponse, response.json())

    async def post_table_rows(
        self,
        doc_id: str,
        table_id: str,
        body: RowsUpsertBody,
        query: RowsUpsertQuery | None = None,
    ) -> RowsUpsertQueuedResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        response = await self.http.post(
            self.url(f"/docs/{d}/tables/{t}/rows"),
            params=self.query_dict(query),
            json=body.model_dump(by_alias=True, exclude_none=True),
        )
        response.raise_for_status()
        return validate_pydantic(RowsUpsertQueuedResponse, response.json())

    async def delete_table_row(
        self,
        doc_id: str,
        table_id: str,
        row_id: str,
    ) -> RowDeleteQueuedResponse:
        d = self._doc(doc_id)
        t = self._seg(table_id)
        r = self._seg(row_id)
        response = await self.http.delete(
            self.url(f"/docs/{d}/tables/{t}/rows/{r}"),
        )
        response.raise_for_status()
        return validate_pydantic(RowDeleteQueuedResponse, response.json())
