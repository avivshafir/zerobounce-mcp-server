# ZeroBounce MCP Server

This is a Model Context Protocol (MCP) server for interacting with the ZeroBounce email validation service. It uses the official [ZeroBounce Python API v2](https://github.com/zerobounce/zerobounce-python-api-v2) library.

## Features

- Validate individual email addresses
- Check your remaining API credits
- Upload files for bulk validation
- Check file status, retrieve, and delete bulk validation files
- Search for email patterns used by a domain

## Setup

### System Requirements

- Python 3.10+
- API key from ZeroBounce

### Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/mcp-zerobounce.git
cd mcp-zerobounce
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables:

   Option 1: Using a .env file (recommended)

   Create a .env file with your ZeroBounce API key:

   ```
   ZEROBOUNCE_API_KEY=your_zerobounce_api_key
   ```

   Option 2: Setting environment variables directly

   ```bash
   export ZEROBOUNCE_API_KEY="your_zerobounce_api_key"
   ```

You can get your API key from your ZeroBounce account dashboard.

Add the following configuration to the `mcp.json` file, replacing the directory path with the actual path to where you've installed this server:

```json
{
  "mcpServers": {
    "zerobounce": {
      "command": "python",
      "args": ["/path/to/your/mcp-zerobounce/main.py"]
    }
  }
}
```

4. Restart Cursor to apply the changes

Now you can use the ZeroBounce MCP server directly within Cursor's AI assistant.

## Available Tools

The server provides the following tools:

1. `validate_email`: Validate a single email address

   ```
   validate_email(email: str, ip_address: str = "") -> dict
   ```

2. `get_credits`: Check remaining credits in your ZeroBounce account

   ```
   get_credits() -> dict
   ```

3. `upload_file`: Upload a file for bulk validation

   ```
   upload_file(file_path: str, email_column: int, ...) -> dict
   ```

4. `check_file_status`: Check the status of a bulk validation file

   ```
   check_file_status(file_id: str) -> dict
   ```

5. `get_file`: Get the results of a bulk validation

   ```
   get_file(file_id: str) -> dict
   ```

6. `delete_file`: Delete a bulk validation file

   ```
   delete_file(file_id: str) -> dict
   ```

7. `domain_search`: Search for email patterns used by a domain
   ```
   domain_search(domain: str) -> dict
   ```

## Dependencies

- zerobounce-python-api-v2: The official ZeroBounce API library
- python-dotenv: For loading environment variables from .env file
- mcp: The Model Context Protocol library
- asyncio: For asynchronous operations
