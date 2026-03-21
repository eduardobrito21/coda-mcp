from fastmcp import FastMCP

from coda_mcp.client import coda_client
from coda_mcp.models import (
    CodaCell,
    CodaRow,
    ColumnListItem,
    PushButtonQueuedResponse,
    RowDeleteQueuedResponse,
    RowListItem,
    RowsDeleteBody,
    RowsDeleteQueuedResponse,
    RowsUpsertBody,
    RowsUpsertQueuedResponse,
    RowUpdateBody,
    TableListItem,
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
    async def get_table(doc_id: str, table_id: str) -> TableListItem:
        """Get metadata and schema for a single Coda table or view."""
        return await coda_client.tables.get_table(doc_id, table_id)

    @mcp.tool()
    async def get_row(doc_id: str, table_id: str, row_id: str) -> RowListItem:
        """Get a single row from a Coda table by row ID."""
        return await coda_client.tables.get_row(doc_id, table_id, row_id)

    @mcp.tool()
    async def update_row(
        doc_id: str,
        table_id: str,
        row_id: str,
        cells: list[CodaCell],
    ) -> RowDeleteQueuedResponse:
        """Update specific cells in an existing row. Only the provided columns are changed."""
        body = RowUpdateBody.model_validate(
            {"row": {"cells": [{"column": c.column, "value": c.value} for c in cells]}}
        )
        return await coda_client.tables.update_row(doc_id, table_id, row_id, body)

    @mcp.tool()
    async def delete_rows(
        doc_id: str,
        table_id: str,
        row_ids: list[str],
    ) -> RowsDeleteQueuedResponse:
        """Delete multiple rows from a Coda table at once."""
        body = RowsDeleteBody.model_validate({"rowIds": row_ids})
        return await coda_client.tables.delete_rows(doc_id, table_id, body)

    @mcp.tool()
    async def delete_row(
        doc_id: str,
        table_id: str,
        row_id: str,
    ) -> RowDeleteQueuedResponse:
        """Delete a single row from a Coda table by row ID."""
        return await coda_client.tables.delete_table_row(doc_id, table_id, row_id)

    @mcp.tool()
    async def push_button(
        doc_id: str,
        table_id: str,
        row_id: str,
        column_id: str,
    ) -> PushButtonQueuedResponse:
        """Execute a button column for a specific row. Use list_columns to find button column IDs."""
        return await coda_client.tables.push_button(doc_id, table_id, row_id, column_id)

    @mcp.tool()
    async def list_columns_typed(doc_id: str, table_id: str) -> list[ColumnListItem]:
        """List all columns in a table including type info. Useful to identify button columns before calling push_button."""
        data = await coda_client.tables.list_columns(doc_id, table_id)
        return data.items
