# coda-io-mcp

A Coda.io MCP server built with FastMCP — expose your Coda docs, pages, and tables to any MCP client.

## Hosted MCP (Prefect Horizon)

This server is deployed on **[Prefect Horizon](https://horizon.prefect.io/)** — managed FastMCP hosting (GitHub builds, HTTPS, auth, monitoring). To change or redeploy it, use the Horizon dashboard.

**Public endpoint:** `https://coda-io.fastmcp.app/mcp`

**HTTP clients (Horizon, `mcp-remote`, Claude Code HTTP):** send your **[Coda API key](https://coda.io/account)** in the **`X-Coda-Api-Key`** header.

**Local stdio** (`uv run coda-mcp`, Cursor with `env`): set **`CODA_API_KEY`** in the environment (or `.env`); custom headers are not used.

### Claude Desktop (connect to Horizon)

Claude Desktop speaks MCP over stdio, so use a small bridge to the remote HTTP server. Add this to `~/Library/Application Support/Claude/claude_desktop_config.json` (Windows: `%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "coda-io": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://coda-io.fastmcp.app/mcp",
        "--header",
        "X-Coda-Api-Key:YOUR_CODA_API_KEY"
      ]
    }
  }
}
```

Replace `YOUR_CODA_API_KEY` with your key from [coda.io/account](https://coda.io/account). Restart Claude Desktop after saving.

### Claude Code (HTTP)

Options (`--transport`, `--header`, `--scope`, …) must come **before** the server name. Example:

```bash
claude mcp add --transport http \
  --header "X-Coda-Api-Key: YOUR_CODA_API_KEY" \
  coda-io https://coda-io.fastmcp.app/mcp
```

Add `--scope project` or `--scope user` if you want a specific config location.

## Features

**Docs**

- **`list_docs`** — List all Coda docs accessible with your API key, with optional name filter
- **`search_docs`** — Search for Coda docs by name or keyword
- **`get_doc`** — Full doc metadata (owner, workspace, published state, etc.)
- **`patch_doc`** — Rename a doc or change its icon
- **`list_doc_categories`** — Category names for publishing to the gallery
- **`publish_doc`** / **`unpublish_doc`** — Publish or unpublish a doc

**Permissions (doc ACL)**

- **`get_sharing_metadata`**, **`list_doc_permissions`**, **`add_doc_permission`**, **`delete_doc_permission`**, **`search_doc_principals`**, **`get_acl_settings`**, **`update_acl_settings`** — Sharing and access control for a doc

**Pages**

- **`list_pages`** — List all pages in a given Coda doc
- **`get_page_metadata`** — Page metadata from the REST API (name, hierarchy, visibility)
- **`list_page_content`** / **`delete_page_content`** — List or delete canvas content elements on a page
- **`export_page_markdown`** — Export a page body as markdown (async export + download)
- **`update_page`** — Replace the full content of a Coda page

**Tables**

- **`list_tables`** — List tables and views in a doc (use before row operations)
- **`list_columns`** — List columns in a table (use before upserts)
- **`list_columns_typed`** — Same as `list_columns` with richer column type info (e.g. button columns)
- **`get_column`** — Metadata for one column by ID or name (same shape as `list_columns_typed` items)
- **`list_rows`** — List rows from a Coda table, with optional query filter and limit
- **`get_table`** — Get metadata and schema for one table or view
- **`get_row`** — Get a single row by row ID
- **`upsert_row`** — Insert or update a row (supports key-column upsert)
- **`update_row`** — Update cells on an existing row
- **`delete_rows`** — Delete multiple rows at once
- **`delete_row`** — Delete one row by row ID
- **`push_button`** — Run a button column for a row

**Structure**

- **`whoami`** — Return details about the Coda account for the current API key
- **`resolve_link`** — Resolve a Coda browser URL to resource type and ID
- **`get_mutation_status`** — Check completion of a queued mutation by `request_id`
- **`list_workspaces`** / **`get_workspace`** — List or fetch Coda workspaces
- **`list_formulas`** / **`get_formula`** — List or read named formulas in a doc
- **`list_controls`** / **`get_control`** — List or read controls (sliders, dropdowns, etc.)

**Creation**

- **`create_doc`** — Create a new doc; optional copy source and folder placement
- **`create_page`** — Create a page with optional markdown and parent page

**Management**

- **`list_folders`** — List workspace folders (for folder IDs when creating docs)
- **`delete_doc`** — Permanently delete a doc (cannot be undone)
- **`delete_page`** — Permanently delete a page (cannot be undone)

**Folders**

- **`create_folder`**, **`get_folder`**, **`patch_folder`**, **`delete_folder`** — Folder CRUD in a workspace

**Analytics**

- **`list_doc_analytics`**, **`list_page_analytics`**, **`get_doc_analytics_summary`**, **`list_pack_analytics`**, **`get_pack_analytics_summary`**, **`list_pack_formula_analytics`**, **`get_analytics_updated`** — Usage analytics (availability depends on your Coda plan and token scopes)

**Automations**

- **`trigger_automation`** — Run a Coda automation with optional payload

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- A Coda API key — get yours at [coda.io/account](https://coda.io/account)

## Local development

Clone the repo and install dependencies with [uv](https://docs.astral.sh/uv/):

```bash
git clone https://github.com/<user>/coda-io-mcp
cd coda-io-mcp
uv sync
cp .env.example .env
# set CODA_API_KEY in .env for local runs
```

Run the stdio server:

```bash
uv run coda-mcp
# or: fastmcp run coda_mcp/server.py
```

For local HTTP (e.g. debugging):

```bash
fastmcp run coda_mcp/server.py --transport http
```

If you deploy your own fork on Horizon, set entrypoint `coda_mcp/server.py:mcp` (same as `fastmcp run`).

### Coda API errors

Failed Coda requests (including **401** and **403** from a missing, invalid, or under-scoped API key) surface as **`ToolError`** messages that include the HTTP status and a snippet of the response body.

### Claude Desktop (local server)

```json
{
  "mcpServers": {
    "coda-io-local": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/coda-io-mcp", "coda-mcp"],
      "env": {
        "CODA_API_KEY": "YOUR_CODA_API_KEY"
      }
    }
  }
}
```

### Claude Code (local stdio)

```bash
claude mcp add --transport stdio --env CODA_API_KEY=YOUR_CODA_API_KEY coda-io-local -- \
  uv run --directory /path/to/coda-io-mcp coda-mcp
```

## Example prompts

- "List all my Coda docs"
- "Search for docs related to project planning"
- "Show me all pages in doc `AbCdEfGh`"
- "Export page `xyz` in doc `AbCdEfGh` as markdown (`export_page_markdown`)"
- "Add a row to the Tasks table in my doc with column Status set to Done"
- "List tables in this doc so I can pick the right table ID"
- "Resolve this Coda URL and open the right resource"

## Tool reference

The tables below list tools exposed by this MCP. The full [Coda OpenAPI v1](https://coda.io/apis/v1/openapi.yaml) specification also covers Packs, custom domains, Go Links, and other org-level features that are not implemented here unless added explicitly.

### Docs

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_docs` | List all accessible Coda docs | `query` (optional filter) |
| `search_docs` | Search docs by name or keyword | `query` |
| `get_doc` | Full doc metadata | `doc_id` |
| `patch_doc` | Rename a doc or change its icon | `doc_id`, `title`, `icon_name` |
| `list_doc_categories` | Publish/gallery categories | — |
| `publish_doc` | Queue publishing a doc | `doc_id`, optional `slug`, `category_names`, … |
| `unpublish_doc` | Unpublish a doc | `doc_id` |

### Permissions

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `get_sharing_metadata` | Whether you can share the doc | `doc_id` |
| `list_doc_permissions` | List access entries | `doc_id`, optional `limit`, `page_token` |
| `add_doc_permission` | Grant access | `doc_id`, `access`, `principal_type`, `principal_email` |
| `delete_doc_permission` | Revoke by permission id | `doc_id`, `permission_id` |
| `search_doc_principals` | Search users/groups to add | `doc_id`, optional `query` |
| `get_acl_settings` | Doc sharing settings | `doc_id` |
| `update_acl_settings` | Update sharing settings | `doc_id`, optional bool flags |

### Pages

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_pages` | List all pages in a doc | `doc_id` |
| `get_page_metadata` | Page metadata (REST) | `doc_id`, `page_id` |
| `list_page_content` | List canvas elements on a page | `doc_id`, `page_id`, optional `limit`, `page_token` |
| `delete_page_content` | Delete some or all content | `doc_id`, `page_id`, optional `element_ids` |
| `export_page_markdown` | Export page body as markdown | `doc_id`, `page_id` |
| `update_page` | Replace full page content | `doc_id`, `page_id`, `content` |

### Tables

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_tables` | List tables and views in a doc | `doc_id` |
| `list_columns` | List columns in a table | `doc_id`, `table_id` |
| `list_columns_typed` | Columns with type info (e.g. buttons) | `doc_id`, `table_id` |
| `get_column` | One column by ID or name | `doc_id`, `table_id`, `column_id` |
| `list_rows` | List rows from a table | `doc_id`, `table_id`, `limit`, `query` |
| `get_table` | Table/view metadata and schema | `doc_id`, `table_id` |
| `get_row` | One row by ID | `doc_id`, `table_id`, `row_id` |
| `upsert_row` | Insert or update a row | `doc_id`, `table_id`, `cells`, `key_columns` |
| `update_row` | Update cells on a row | `doc_id`, `table_id`, `row_id`, `cells` |
| `delete_rows` | Delete multiple rows | `doc_id`, `table_id`, `row_ids` |
| `delete_row` | Delete one row | `doc_id`, `table_id`, `row_id` |
| `push_button` | Execute a button column | `doc_id`, `table_id`, `row_id`, `column_id` |

### Structure

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `whoami` | Account details for the API key | — |
| `resolve_link` | Resolve a Coda URL to resource metadata | `url` |
| `get_mutation_status` | Status of a queued mutation | `request_id` |
| `list_workspaces` | List workspaces | — |
| `get_workspace` | One workspace by ID | `workspace_id` |
| `list_formulas` | List named formulas in a doc | `doc_id` |
| `get_formula` | Read one formula | `doc_id`, `formula_id_or_name` |
| `list_controls` | List controls in a doc | `doc_id` |
| `get_control` | Read one control | `doc_id`, `control_id_or_name` |

### Creation

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `create_doc` | Create a new doc | `title`, `source_doc_id`, `folder_id` |
| `create_page` | Create a page (optional markdown, parent) | `doc_id`, `name`, `content`, `parent_page_id` |

### Management

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_folders` | List folders in the workspace | `workspace_id` |
| `delete_doc` | Permanently delete a doc | `doc_id` |
| `delete_page` | Permanently delete a page | `doc_id`, `page_id` |

### Folders

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `create_folder` | Create a folder | `name`, `workspace_id`, optional `description` |
| `get_folder` | Folder metadata | `folder_id` |
| `patch_folder` | Rename or change description | `folder_id`, `name`, `description` |
| `delete_folder` | Delete a folder | `folder_id` |

### Analytics

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_doc_analytics` | Per-doc analytics | optional filters (`limit`, `workspace_id`, `doc_ids`, …) |
| `list_page_analytics` | Per-page analytics | `doc_id`, optional `limit`, `page_token`, dates |
| `get_doc_analytics_summary` | Aggregated doc metrics | optional filters |
| `list_pack_analytics` | Pack usage | optional filters |
| `get_pack_analytics_summary` | Aggregated Pack metrics | optional `pack_ids`, … |
| `list_pack_formula_analytics` | Per-formula Pack stats | `pack_id`, optional filters |
| `get_analytics_updated` | Last-updated timestamps for datasets | — |

### Automations

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `trigger_automation` | Run an automation | `doc_id`, `automation_id`, `payload` |

## Contributing

Contributions are welcome! Open an issue or submit a pull request for bug fixes, new tools, or improvements. Please keep PRs focused and include a clear description of the change.

## License

MIT — Copyright Eduardo Brito 2026
