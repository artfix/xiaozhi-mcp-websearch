# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Workflow

| Task | Command | Notes |
|------|---------|-------|
| Install dependencies | `pip install -r requirements.txt` | Use a virtual environment to avoid polluting the system Python. |
| Run the MCP server | `python mcp_pipe.py websitesearch.py` | This launches the WebSocket connector and starts the `websitesearch.py` subprocess. The script will automatically reconnect on failure. |
| Test the search tool manually | `python -m mcp.run websitesearch.py --transport=stdio` | The `websitesearch.py` module registers a `websitesearch` tool; you can invoke it through the FastMCP CLI to see raw output. |
| Run unit tests (if added) | `pytest` | No tests are currently committed; add tests under `tests/` and run with `pytest`. |

## Code Architecture Overview

1. **`mcp_pipe.py`** – A lightweight WebSocket bridge. It connects to the specified MCP endpoint, spawns a subprocess running `websitesearch.py`, and forwards messages bi‑directionally.
   * `pipe_websocket_to_process` reads messages from the MCP socket and writes them to the subprocess’s stdin.
   * `pipe_process_to_websocket` streams the subprocess stdout back to the MCP socket.
   * The loop automatically reconnects with exponential back‑off on failure.

2. **`websitesearch.py`** – Implements the actual search logic as an MCP tool.
   * Uses `FastMCP` to register a `websitesearch` tool.
   * The tool queries Baidu for the given query, filters results to the current year, extracts timestamps, and formats a concise spoken‑style response.
   * `extract_and_validate_time` parses Chinese date formats and relative times.
   * Results are sorted by recency and limited to the three most recent entries.

3. **Dependencies** – The project relies on `fastmcp` (the MCP runtime), `aiohttp` for HTTP requests, `beautifulsoup4` for parsing Baidu results, and `websockets` for the connector.

## Common Pitfalls

* The MCP token in `mcp_pipe.py` is hard‑coded. For production, replace the placeholder with a real token or read from an environment variable.
* Baidu’s HTML structure can change. If search results stop parsing, inspect the page with `requests` and adjust the CSS selectors in `websitesearch.py`.
* Ensure the system has network access; the connector and search rely on external HTTP endpoints.

## Extending the Project

* **Add more tools** – Duplicate the pattern in `websitesearch.py`: create a new function, decorate it with `@mcp.tool()`, and register it with `FastMCP`.
* **Improve result filtering** – Currently only the current year is considered. Expand `extract_and_validate_time` to support other date ranges or languages.
* **Testing** – Mock `aiohttp` and `beautifulsoup4` responses to unit‑test the parsing logic.

---

*Feel free to adjust the commands or add more sections that are relevant for your workflow.*