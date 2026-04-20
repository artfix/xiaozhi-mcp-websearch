# DuckDuckGo Search CLI

This repository contains a tiny, self‑contained DuckDuckGo web‑search utility written in Python. It fetches search results, extracts dates from titles or snippets (only for the current year), and returns up to 20 concise results in JSON form. The utility is designed to be used as an MCP (Machine‑Readable, Command‑Based Protocol) tool, but can also be run as a regular Python script for quick experimentation.

## Features

- **Year‑aware filtering** – Only keeps snippets that mention a date in the current year. If no date is found, the result is tagged with the current time.
- **Top‑N results** – Return the most recent 20 results (configurable in the source).
- **Minimal dependencies** – Built on `aiohttp` for async HTTP requests and `BeautifulSoup` for parsing.
- **MCP compatible** – Exposes a `websitesearch` RPC that can be consumed by other MCP clients.

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-org>/xiaozhi-mcp-websearch.git
cd xiaozhi-mcp-websearch

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

`requirements.txt` should contain:

```text
aiohttp==3.9.3
beautifulsoup4==4.12.3
```

If you prefer to use `pip` directly:

```bash
pip install aiohttp beautifulsoup4
```

## Usage

### Running the MCP tool

```bash
python websitesearch.py
```

The script will start an MCP server on STDIO. You can invoke the `websitesearch` method via any MCP client. Example JSON request:

```json
{
  "query": "latest version of ollama"
}
```

The response will be:

```json
{
  "success": true,
  "result": [
    "Ollama 0.3.0 – the newest Docker‑based LLM runtime（近日）",
    "Official Ollama release notes – version 0.3.0（6月15日）",
    "…",
    "…"
  ]
}
```

### Quick local test

You can also run the script directly to see the results in the console:

```bash
python websitesearch.py
# Then input a query when prompted.
```

The console will print up to 20 formatted snippets.

## Extending the Project

- **Increase the result limit** – Adjust the slice in `websitesearch` (currently `[:20]`).
- **Add more filters** – Modify `extract_and_validate_time` to support other date formats.
- **Integrate with a larger system** – Expose the tool via `FastMCP` for use in a micro‑service.

## License

This project is released under the MIT license. See the `LICENSE` file for details.

---

> *Author: John (xiaozhi‑mcp‑websearch)*

