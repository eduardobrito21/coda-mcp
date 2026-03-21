from fastmcp import FastMCP

from coda_mcp.client import coda_client
from coda_mcp.models import (
    CodaCell,
    CodaRow,
    RowDeleteQueuedResponse,
    RowsUpsertBody,
    RowsUpsertQueuedResponse,
    TableRowsQuery,
)


def register(mcp: FastMCP) -> None:

    @mcp.tool()
    async def list_rows(
        doc_id: str,
        table_id: str,
        limit: int = 25,
        query: str = "",
    ) -> list[CodaRow]:
        """List rows from a Coda table. Optionally filter with a query string."""
        row_q: dict[str, object] = {
            "limit": limit,
            "valueFormat": "simpleWithArrays",
        }
        if query:
            row_q["query"] = query
        params = TableRowsQuery.model_validate(row_q)
        data = await coda_client.tables.get_table_rows(doc_id, table_id, params)
        return [CodaRow(id=r.id, name=r.name, values=r.values) for r in data.items]

    @mcp.tool()
    async def upsert_row(
        doc_id: str,
        table_id: str,
        cells: list[CodaCell],
        key_columns: list[str] | None = None,
    ) -> RowsUpsertQueuedResponse:
        """Insert or update a row in a Coda table.

        Provide key_columns to upsert instead of always inserting.
        """
        body = RowsUpsertBody.model_validate(
            {
                "rows": [
                    {
                        "cells": [{"column": c.column, "value": c.value} for c in cells],
                    },
                ],
                "keyColumns": key_columns or [],
            },
        )
        return await coda_client.tables.post_table_rows(doc_id, table_id, body)

    @mcp.tool()
    async def delete_row(
        doc_id: str,
        table_id: str,
        row_id: str,
    ) -> RowDeleteQueuedResponse:
        """Delete a row from a Coda table by row ID."""
        return await coda_client.tables.delete_table_row(doc_id, table_id, row_id)
