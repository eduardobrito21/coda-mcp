---
name: coda-io-mcp
description: >-
  How to use the coda-io-mcp Model Context Protocol server with Coda.io. Apply
  when the user connects this MCP, asks to read/write Coda docs, pages, or
  tables, shares a coda.io URL, or needs workspace sharing, analytics, or
  automations via tools named like list_docs, list_rows, or resolve_link.
---

# Coda.io MCP (coda-io-mcp)

This skill teaches how to drive **coda-io-mcp** tools: a FastMCP server that wraps the **[Coda REST API v1](https://coda.io/apis/v1/openapi.yaml)** so assistants can work with **docs**, **pages**, and **tables** programmatically.

## Coda concepts (short)

- A **doc** is a collaborative workspace: narrative content **pages** plus structured **tables** (and views), **controls**, and **named formulas**. Product learning material lives in [Coda resources](https://coda.io/resources) (guides, courses, help center, [formula list](https://coda.io/formulas)).
- Identifiers are opaque strings (e.g. doc, page, table, row IDs). Prefer **`resolve_link`** when the user pastes a browser URL so you get the correct resource type and IDs.

## Authentication

| Transport | How the Coda API key is supplied |
|----------|-----------------------------------|
| **HTTP** (hosted MCP, `mcp-remote`, Claude Code `--transport http`) | Header **`X-Coda-Api-Key`** with the key from [coda.io/account](https://coda.io/account). |
| **stdio** (local `uv run coda-mcp`, Cursor env) | Environment variable **`CODA_API_KEY`** (e.g. `.env`); custom headers are not used. |

If no key is configured, tools fail with a clear error about a missing API key. **401/403** usually mean a missing, invalid, or under-scoped key.

## Recommended workflows

### Orient and disambiguate

1. **`whoami`** — Confirm which account the key represents.
2. **`resolve_link`** — If the user gave a `coda.io` URL, resolve it before guessing IDs.
3. **`list_docs`** / **`search_docs`** — Find the target doc when you only have a name or keyword.

### Pages and export

1. **`list_pages`** — Discover `page_id`s and hierarchy.
2. **`get_page_metadata`** — Names, parent page, visibility.
3. **`export_page_markdown`** — Full page body as markdown (async export + download).
4. **`list_page_content`** / **`delete_page_content`** — Fine-grained canvas elements.
5. **`update_page`** — Replace entire page content (destructive; confirm intent).

### Tables and rows

1. **`list_tables`** — Tables and views in the doc (always do this before row ops).
2. **`get_table`** — Schema and metadata for one table or view.
3. **`list_columns`** or **`list_columns_typed`** — Column IDs/names; use **typed** when you need button columns or richer types.
4. **`get_column`** — One column by ID or name.
5. **`list_rows`** — Read data; optional query filter and limit.
6. **`get_row`** — Single row by ID.
7. Writes: **`upsert_row`** (optional key columns), **`update_row`**, **`delete_row`** / **`delete_rows`**.
8. **`push_button`** — Execute a **button** column for a row (after identifying the button column from **`list_columns_typed`**).

After writes that queue on the server, use **`get_mutation_status`** with the returned **`request_id`** when you need to confirm completion.

### Docs, publishing, and ACL

- **Metadata / rename / icon:** **`get_doc`**, **`patch_doc`**.
- **Gallery:** **`list_doc_categories`**, **`publish_doc`**, **`unpublish_doc`**.
- **Sharing:** **`get_sharing_metadata`**, **`list_doc_permissions`**, **`add_doc_permission`**, **`delete_doc_permission`**, **`search_doc_principals`**, **`get_acl_settings`**, **`update_acl_settings`**.

### Creation and workspace layout

- **`create_doc`** — New doc; optional copy source and **`folder_id`**.
- **`list_workspaces`**, **`get_workspace`**, **`list_folders`**, folder tools (**`create_folder`**, **`get_folder`**, **`patch_folder`**, **`delete_folder`**) — Place and organize docs.
- **`create_page`** — New page; optional markdown and parent page.

### Structure helpers

- **`list_formulas`** / **`get_formula`**, **`list_controls`** / **`get_control`** — Read named formulas and doc controls (sliders, selects, etc.).

### Analytics and automations

- **Analytics** tools (`list_doc_analytics`, `list_page_analytics`, summaries, pack analytics, **`get_analytics_updated`**) — Availability depends on **Coda plan** and **token/API scopes**; handle “not available” or permission errors gracefully.
- **`trigger_automation`** — Run a Coda automation with optional **`payload`**.

### Destructive operations

- **`delete_doc`**, **`delete_page`**, **`delete_folder`** — **Permanent**; only after explicit user confirmation.

## Errors

Failed Coda HTTP calls surface as **`ToolError`** (or similar) messages that include **status code** and a **snippet of the response body**—use them to explain auth, not-found, validation, or scope issues to the user.

## Hosted vs local (operator reference)

- **Hosted example** (see project `README.md`): MCP URL `https://coda-io.fastmcp.app/mcp` with **`X-Coda-Api-Key`**.
- **Local**: `uv run coda-mcp` with **`CODA_API_KEY`** set.

## What this MCP does not cover

The [Coda OpenAPI](https://coda.io/apis/v1/openapi.yaml) includes org features (e.g. some Packs, custom domains, Go Links) that may not be exposed as tools until implemented in the server—if a tool is missing, say so and suggest the REST API or Coda UI.
