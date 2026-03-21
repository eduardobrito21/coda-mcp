# coda-io-mcp

A Coda.io MCP server built with FastMCP — expose your Coda docs, pages, and tables to any MCP client.

## Features

**Docs**

- **`list_docs`** — List all Coda docs accessible with your API key, with optional name filter
- **`search_docs`** — Search for Coda docs by name or keyword
- **`patch_doc`** — Rename a doc or change its icon

**Pages**

- **`list_pages`** — List all pages in a given Coda doc
- **`get_page`** — Retrieve the full content of a Coda page as markdown
- **`update_page`** — Replace the full content of a Coda page

**Tables**

- **`list_tables`** — List tables and views in a doc (use before row operations)
- **`list_columns`** — List columns in a table (use before upserts)
- **`list_rows`** — List rows from a Coda table, with optional query filter and limit
- **`upsert_row`** — Insert or update a row in a Coda table (supports key-column upsert)
- **`delete_row`** — Delete a row from a Coda table by row ID

**Structure**

- **`whoami`** — Return details about the Coda account for the current API key
- **`resolve_link`** — Resolve a Coda browser URL to resource type and ID
- **`get_mutation_status`** — Check completion of a queued mutation by `request_id`

**Creation**

- **`create_doc`** — Create a new doc; optional copy source and folder placement
- **`create_page`** — Create a page with optional markdown and parent page

**Management**

- **`list_folders`** — List workspace folders (for folder IDs when creating docs)
- **`delete_doc`** — Permanently delete a doc (cannot be undone)
- **`delete_page`** — Permanently delete a page (cannot be undone)

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- A Coda API key — get yours at [coda.io/account](https://coda.io/account)

## Installation

```bash
git clone https://github.com/<user>/coda-io-mcp
cd coda-io-mcp
uv sync
cp .env.example .env
# edit .env and add your CODA_API_KEY
```

## Claude Desktop setup

Add the following to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "coda": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/coda-io-mcp", "coda-mcp"],
      "env": {
        "CODA_API_KEY": "your_token_here"
      }
    }
  }
}
```

## Claude Code setup

```bash
claude mcp add coda -e CODA_API_KEY=your_token_here -- uv run --directory /path/to/coda-io-mcp coda-mcp
```

## Example prompts

- "List all my Coda docs"
- "Search for docs related to project planning"
- "Show me all pages in doc `AbCdEfGh`"
- "Get the content of page `xyz` in doc `AbCdEfGh`"
- "Add a row to the Tasks table in my doc with column Status set to Done"
- "List tables in this doc so I can pick the right table ID"
- "Resolve this Coda URL and open the right resource"

## Tool reference

### Docs

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_docs` | List all accessible Coda docs | `query` (optional filter) |
| `search_docs` | Search docs by name or keyword | `query` |
| `patch_doc` | Rename a doc or change its icon | `doc_id`, `title`, `icon_name` |

### Pages

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_pages` | List all pages in a doc | `doc_id` |
| `get_page` | Get page content as markdown | `doc_id`, `page_id` |
| `update_page` | Replace full page content | `doc_id`, `page_id`, `content` |

### Tables

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_tables` | List tables and views in a doc | `doc_id` |
| `list_columns` | List columns in a table | `doc_id`, `table_id` |
| `list_rows` | List rows from a table | `doc_id`, `table_id`, `limit`, `query` |
| `upsert_row` | Insert or update a row | `doc_id`, `table_id`, `cells`, `key_columns` |
| `delete_row` | Delete a row by ID | `doc_id`, `table_id`, `row_id` |

### Structure

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `whoami` | Account details for the API key | — |
| `resolve_link` | Resolve a Coda URL to resource metadata | `url` |
| `get_mutation_status` | Status of a queued mutation | `request_id` |

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

## Contributing

Contributions are welcome! Open an issue or submit a pull request for bug fixes, new tools, or improvements. Please keep PRs focused and include a clear description of the change.

## License

MIT — Copyright Eduardo Brito 2026
