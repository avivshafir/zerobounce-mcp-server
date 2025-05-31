import os
import asyncio
import logging
from typing import Dict, List, Optional, Any, Annotated

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context

from zerobounce_api import ZeroBounceAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create the FastMCP instance
mcp = FastMCP("ZeroBounce MCP")

# Store the API client globally
api = None


def init_api():
    """Initialize the ZeroBounce API client."""
    global api
    api_key = os.getenv("ZEROBOUNCE_API_KEY")
    if not api_key:
        logger.error("ZEROBOUNCE_API_KEY environment variable not set")
        raise ValueError("ZEROBOUNCE_API_KEY environment variable is required")

    # Check if SSL verification should be disabled (for development only)
    verify_ssl = False

    if not verify_ssl:
        logger.warning(
            "SSL verification disabled. This should only be used in development environments."
        )

    api = ZeroBounceAPI(api_key, verify_ssl=verify_ssl)
    return api


@mcp.tool()
async def validate_email(
    context: Context,
    email: Annotated[str, "The email address to validate"],
    ip_address: Annotated[
        str, "The IP address the email signed up from (optional)"
    ] = "",
) -> Dict[str, Any]:
    """Validate a single email address using the ZeroBounce API."""
    try:
        global api
        if not api:
            api = init_api()
        result = await api.validate_email(email, ip_address)
        return result
    except Exception as e:
        logger.error(f"Error validating email: {e}")
        return {"error": str(e)}


@mcp.tool()
async def get_credits(context: Context) -> Dict[str, Any]:
    """Get the number of credits remaining in your ZeroBounce account."""
    try:
        global api
        if not api:
            api = init_api()
        result = await api.get_credits()
        return result
    except Exception as e:
        logger.error(f"Error getting credits: {e}")
        return {"error": str(e)}


@mcp.tool()
async def upload_file(
    context: Context,
    file_path: Annotated[
        str, "The path to the file to upload (.csv, .txt, .xls, or .xlsx)"
    ],
    email_column: Annotated[
        int, "The column index of the email address in your file (starts from 1)"
    ],
    first_name_column: Annotated[
        int, "The column index of the first name column (optional)"
    ] = 0,
    last_name_column: Annotated[
        int, "The column index of the last name column (optional)"
    ] = 0,
    gender_column: Annotated[
        int, "The column index of the gender column (optional)"
    ] = 0,
    ip_address_column: Annotated[
        int, "The column index of the IP address column (optional)"
    ] = 0,
    has_header_row: Annotated[
        bool, "Whether the first row is a header row (optional)"
    ] = True,
    return_url: Annotated[
        str, "The URL to call back when validation is complete (optional)"
    ] = "",
) -> Dict[str, Any]:
    """Upload a file for bulk email validation."""
    try:
        global api
        if not api:
            api = init_api()
        result = await api.upload_file(
            file_path=file_path,
            email_column=email_column,
            first_name_column=first_name_column,
            last_name_column=last_name_column,
            gender_column=gender_column,
            ip_address_column=ip_address_column,
            has_header_row=has_header_row,
            return_url=return_url,
        )
        return result
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return {"error": str(e)}


@mcp.tool()
async def check_file_status(
    context: Context, file_id: Annotated[str, "The ID of the file to check status for"]
) -> Dict[str, Any]:
    """Check the status of a bulk email validation file."""
    try:
        global api
        if not api:
            api = init_api()
        result = await api.check_file_status(file_id)
        return result
    except Exception as e:
        logger.error(f"Error checking file status: {e}")
        return {"error": str(e)}


@mcp.tool()
async def get_file(
    context: Context, file_id: Annotated[str, "The ID of the file to get results for"]
) -> Dict[str, Any]:
    """Get the validation results file for a bulk email validation."""
    try:
        global api
        if not api:
            api = init_api()
        result = await api.get_file(file_id)
        return result
    except Exception as e:
        logger.error(f"Error getting file: {e}")
        return {"error": str(e)}


@mcp.tool()
async def delete_file(
    context: Context, file_id: Annotated[str, "The ID of the file to delete"]
) -> Dict[str, Any]:
    """Delete a bulk email validation file."""
    try:
        global api
        if not api:
            api = init_api()
        result = await api.delete_file(file_id)
        return result
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        return {"error": str(e)}


@mcp.tool()
async def domain_search(
    context: Context,
    domain: Annotated[str, "The domain name to search for email patterns"],
) -> Dict[str, Any]:
    """Search for email patterns used by a domain. Note: Use guess_format tool instead for better results."""
    try:
        global api
        if not api:
            api = init_api()
        result = await api.domain_search(domain)
        return result
    except Exception as e:
        logger.error(f"Error searching domain: {e}")
        return {"error": str(e)}


@mcp.tool()
async def guess_format(
    context: Context,
    domain: Annotated[str, "The email domain for which to find the email format"],
    first_name: Annotated[
        str, "The first name of the person whose email format is being searched"
    ],
    middle_name: Annotated[
        str,
        "The middle name of the person whose email format is being searched (optional)",
    ] = "",
    last_name: Annotated[
        str,
        "The last name of the person whose email format is being searched (optional)",
    ] = "",
) -> Dict[str, Any]:
    """Identify the correct email format when you provide a name and email domain."""
    try:
        global api
        if not api:
            api = init_api()
        result = await api.guess_format(domain, first_name, middle_name, last_name)
        return result
    except Exception as e:
        logger.error(f"Error guessing email format: {e}")
        return {"error": str(e)}


async def main():
    # Initialize the API client
    init_api()

    # Run the server with stdio transport
    await mcp.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())
