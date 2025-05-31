#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import ssl
import logging
import asyncio
import tempfile
import warnings
from typing import Dict, Any, Optional

from zerobouncesdk import ZeroBounce, ZBException

logger = logging.getLogger(__name__)


class ZeroBounceAPI:
    """Async client wrapper for the ZeroBounce API using the official zerobouncesdk library."""

    def __init__(self, api_key: str, verify_ssl: bool = False):
        """Initialize the ZeroBounce API client.

        Args:
            api_key (str): Your ZeroBounce API key
            verify_ssl (bool, optional): Whether to verify SSL certificates.
        """
        self.api_key = api_key
        self.verify_ssl = verify_ssl

        # Handle SSL verification if disabled
        if not verify_ssl:
            logger.warning(
                "SSL verification disabled. This should only be used in development environments."
            )
            self._disable_ssl_verification()

        # Initialize the official API client
        self.zero_bounce = ZeroBounce(api_key)

    def _disable_ssl_verification(self):
        """Disable SSL verification using environment variables."""
        try:
            # Set environment variables to disable SSL verification
            os.environ["PYTHONHTTPSVERIFY"] = "0"
            os.environ["CURL_CA_BUNDLE"] = ""

            # Disable urllib3 SSL warnings
            import urllib3

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            logger.info("SSL verification environment variables set")

        except Exception as e:
            logger.warning(f"Could not set SSL environment variables: {e}")

    async def validate_email(self, email: str, ip_address: str = "") -> Dict[str, Any]:
        """Validate a single email address.

        Args:
            email (str): The email address to validate
            ip_address (str, optional): The IP address the email signed up from

        Returns:
            Dict[str, Any]: Validation results
        """
        try:
            # Run the synchronous API call in a thread pool
            if ip_address:
                result = await asyncio.to_thread(
                    self.zero_bounce.validate, email, ip_address
                )
            else:
                result = await asyncio.to_thread(self.zero_bounce.validate, email)

            # Convert response object to dictionary
            if hasattr(result, "__dict__"):
                return result.__dict__
            elif isinstance(result, dict):
                return result
            else:
                return {"result": str(result)}

        except ZBException as e:
            logger.error(f"ZeroBounce API error validating email: {e}")
            return {"error": str(e), "error_type": "ZBException"}
        except ssl.SSLError as e:
            if not self.verify_ssl:
                logger.error(f"SSL error despite disabled verification: {e}")
                return {
                    "error": f"SSL certificate verification failed: {e}",
                    "error_type": "SSLError",
                    "suggestion": "Try running with SSL verification enabled or check your system's SSL configuration",
                }
            else:
                logger.error(f"SSL error: {e}")
                return {"error": str(e), "error_type": "SSLError"}
        except Exception as e:
            logger.error(f"Error validating email: {e}")
            return {"error": str(e), "error_type": "Exception"}

    async def get_credits(self) -> Dict[str, Any]:
        """Get the number of credits remaining in your account.

        Returns:
            Dict[str, Any]: Credit information
        """
        try:
            # Run the synchronous API call in a thread pool
            result = await asyncio.to_thread(self.zero_bounce.get_credits)

            # Convert response to dictionary format
            if hasattr(result, "__dict__"):
                return result.__dict__
            elif isinstance(result, dict):
                return result
            elif isinstance(result, (int, float)):
                return {"credits": result}
            else:
                return {"credits": str(result)}

        except ZBException as e:
            logger.error(f"ZeroBounce API error getting credits: {e}")
            return {"error": str(e), "error_type": "ZBException"}
        except ssl.SSLError as e:
            if not self.verify_ssl:
                logger.error(f"SSL error despite disabled verification: {e}")
                return {
                    "error": f"SSL certificate verification failed: {e}",
                    "error_type": "SSLError",
                    "suggestion": "Try running with SSL verification enabled or check your system's SSL configuration",
                }
            else:
                logger.error(f"SSL error: {e}")
                return {"error": str(e), "error_type": "SSLError"}
        except Exception as e:
            logger.error(f"Error getting credits: {e}")
            return {"error": str(e), "error_type": "Exception"}

    async def upload_file(
        self,
        file_path: str,
        email_column: int,
        first_name_column: int = 0,
        last_name_column: int = 0,
        gender_column: int = 0,
        ip_address_column: int = 0,
        has_header_row: bool = True,
        return_url: str = "",
    ) -> Dict[str, Any]:
        """Upload a file for bulk email validation.

        Args:
            file_path (str): Path to the file to upload
            email_column (int): Column index of the email address (starts from 1)
            first_name_column (int, optional): Column index of the first name
            last_name_column (int, optional): Column index of the last name
            gender_column (int, optional): Column index of the gender
            ip_address_column (int, optional): Column index of the IP address
            has_header_row (bool, optional): Whether the file has a header row
            return_url (str, optional): URL to call when validation is complete

        Returns:
            Dict[str, Any]: Upload response
        """
        try:
            logger.info(f"Uploading file {file_path}")

            # Run the synchronous API call in a thread pool
            # Use 0 for unused columns as per SDK documentation
            result = await asyncio.to_thread(
                self.zero_bounce.send_file,
                file_path,
                email_column,  # email_address_column
                return_url,
                first_name_column if first_name_column > 0 else 0,
                last_name_column if last_name_column > 0 else 0,
                gender_column if gender_column > 0 else 0,
                ip_address_column if ip_address_column > 0 else 0,
                has_header_row,
                True,  # remove_duplicate
            )

            # Convert response to dictionary
            if hasattr(result, "__dict__"):
                return result.__dict__
            elif isinstance(result, dict):
                return result
            else:
                return {"result": str(result)}

        except ZBException as e:
            logger.error(f"ZeroBounce API error uploading file: {e}")
            return {"error": str(e), "error_type": "ZBException"}
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return {"error": str(e), "error_type": "Exception"}

    async def check_file_status(self, file_id: str) -> Dict[str, Any]:
        """Check the status of a bulk email validation file.

        Args:
            file_id (str): ID of the file to check

        Returns:
            Dict[str, Any]: File status
        """
        try:
            # Run the synchronous API call in a thread pool
            result = await asyncio.to_thread(self.zero_bounce.file_status, file_id)

            # Convert response to dictionary
            if hasattr(result, "__dict__"):
                return result.__dict__
            elif isinstance(result, dict):
                return result
            else:
                return {"result": str(result)}

        except ZBException as e:
            logger.error(f"ZeroBounce API error checking file status: {e}")
            return {"error": str(e), "error_type": "ZBException"}
        except Exception as e:
            logger.error(f"Error checking file status: {e}")
            return {"error": str(e), "error_type": "Exception"}

    async def get_file(self, file_id: str) -> Dict[str, Any]:
        """Get the validation results file for a bulk email validation.

        Args:
            file_id (str): ID of the file to get results for

        Returns:
            Dict[str, Any]: File information and download details
        """
        try:
            # Create a temporary file for download
            with tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, suffix=".csv"
            ) as temp_file:
                temp_path = temp_file.name

            logger.info(f"Downloading file {file_id} to {temp_path}")

            # Run the synchronous API call in a thread pool
            result = await asyncio.to_thread(
                self.zero_bounce.get_file, file_id, temp_path
            )

            # Check if file was downloaded successfully
            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                file_size = os.path.getsize(temp_path)
                response: Dict[str, Any] = {
                    "success": True,
                    "file_id": file_id,
                    "local_file_path": temp_path,
                    "file_size": file_size,
                    "message": f"File downloaded successfully to {temp_path}",
                }

                # Include SDK response if available
                if hasattr(result, "__dict__"):
                    response["sdk_response"] = result.__dict__
                elif isinstance(result, dict):
                    response["sdk_response"] = result

                return response
            else:
                return {
                    "error": "File download failed or file is empty",
                    "file_id": file_id,
                    "local_file_path": temp_path,
                }

        except ZBException as e:
            logger.error(f"ZeroBounce API error getting file: {e}")
            return {"error": str(e), "error_type": "ZBException"}
        except Exception as e:
            logger.error(f"Error getting file: {e}")
            return {"error": str(e), "error_type": "Exception"}

    async def delete_file(self, file_id: str) -> Dict[str, Any]:
        """Delete a bulk email validation file.

        Args:
            file_id (str): ID of the file to delete

        Returns:
            Dict[str, Any]: Deletion response
        """
        try:
            # Run the synchronous API call in a thread pool
            result = await asyncio.to_thread(self.zero_bounce.delete_file, file_id)

            # Convert response to dictionary
            if hasattr(result, "__dict__"):
                return result.__dict__
            elif isinstance(result, dict):
                return result
            else:
                return {"result": str(result), "file_id": file_id}

        except ZBException as e:
            logger.error(f"ZeroBounce API error deleting file: {e}")
            return {"error": str(e), "error_type": "ZBException"}
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return {"error": str(e), "error_type": "Exception"}

    async def domain_search(self, domain: str) -> Dict[str, Any]:
        """Search for email patterns used by a domain.

        Note: This method is deprecated. Use guess_format instead for better results.

        Args:
            domain (str): The domain name to search for email patterns

        Returns:
            Dict[str, Any]: Domain search results
        """
        logger.warning(
            "domain_search is deprecated. Use guess_format instead for better results."
        )

        # The official SDK doesn't have a domain_search method
        # Return a helpful message directing users to guess_format
        return {
            "error": "domain_search method is not available in the official SDK",
            "suggestion": "Use guess_format method instead",
            "domain": domain,
        }

    async def guess_format(
        self, domain: str, first_name: str, middle_name: str = "", last_name: str = ""
    ) -> Dict[str, Any]:
        """Identify the correct email format when you provide a name and email domain.

        Args:
            domain (str): The email domain for which to find the email format
            first_name (str): The first name of the person
            middle_name (str, optional): The middle name of the person
            last_name (str, optional): The last name of the person

        Returns:
            Dict[str, Any]: Email format guess results
        """
        try:
            # Run the synchronous API call in a thread pool
            result = await asyncio.to_thread(
                self.zero_bounce.guess_format,
                domain,
                first_name,
                middle_name,
                last_name,
            )

            # Convert response to dictionary
            if hasattr(result, "__dict__"):
                return result.__dict__
            elif isinstance(result, dict):
                return result
            else:
                return {"result": str(result)}

        except ZBException as e:
            logger.error(f"ZeroBounce API error guessing format: {e}")
            return {"error": str(e), "error_type": "ZBException"}
        except Exception as e:
            logger.error(f"Error guessing format: {e}")
            return {"error": str(e), "error_type": "Exception"}

    async def close(self):
        """Close the API client and clean up resources."""
        # The official SDK doesn't require explicit cleanup
        logger.info("ZeroBounce API client closed")
        pass
