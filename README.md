# DuckDuckGo local Search Engine for xiaozhi cloud devices

This repository contains a tiny, self‑contained DuckDuckGo web‑search utility written in Python that enable web search free, we all know that xiaozhi.me devices dont have search nor the cloud service. 
It fetches search results, extracts dates from titles or snippets (only for the current year), and returns up to 20 concise results in JSON form. The utility is designed to be used as an MCP (Machine‑Readable, Command‑Based Protocol) tool, but can also be run as a regular Python script for quick experimentation.

## Features

- **Year‑aware filtering** – Only keeps snippets that mention a date in the current year. If no date is found, the result is tagged with the current time.
- **Top‑N results** – Return the most recent 20 results (configurable in the source).
- **Minimal dependencies** – Built on `aiohttp` for async HTTP requests and `BeautifulSoup` for parsing.
- **MCP compatible** – Exposes a `websitesearch` RPC that can be consumed by other MCP clients EXAMPLE: xiaozhi.me cloud server.

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

## Usage

Open the `mcp_pipe.py` replace in line 11 with your xiaozhi.me token 

`wss://api.xiaozhi.me/mcp/?token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c5VySWQiOjY3Njk4NCwiYWdlbnRJZCI6MTYyNjg3OSwiZW5kcG9pbnRJZCI6ImFnZW50XzE2MjY4NzkiLCJwdXJwb3NlIjoibWNwLWVuZHBvaW50IiwiaWF0IjoxNzc2Njk0Nzk5LCJleHAiOjE4MDgyNTIzOTl9.EZmZU9lNL-psCSzThA-QHC2TRBgV1-Gxszs2QXShncLPCVl1OG3l65foTUu2huf4g4r7AnPFFNj_LKyZFtR1Qw`

save and exit

### Running the MCP tool

```bash
python mcp_pipe.py websitesearch.py
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

> *Author edit: ArtFix (xiaozhi‑mcp‑websearch)*

