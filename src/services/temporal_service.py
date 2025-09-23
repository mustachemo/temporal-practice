"""Temporal service for workflow management."""

# ================================== Imports ================================== #
# Standard Library
import os
from typing import Optional

# Third-party
from temporalio.client import Client
import logging

# ================================== Global Variables ========================= #
_temporal_client: Optional[Client] = None


# ================================== Functions ================================ #
async def get_temporal_client() -> Client:
    """Get Temporal client instance.

    Returns:
        Temporal client instance.

    Raises:
        RuntimeError: If client connection fails.
    """
    global _temporal_client

    if _temporal_client is None:
        try:
            # Get connection details from environment variable
            temporal_host = os.getenv("TEMPORAL_HOST", "localhost:7233")
            _temporal_client = await Client.connect(temporal_host)
                logging.getLogger(__name__).info(f"Connected to Temporal server at {temporal_host}")
        except Exception as e:
                logging.getLogger(__name__).error(f"Failed to connect to Temporal server: {e}")
            raise RuntimeError(f"Failed to connect to Temporal server: {e}")

    return _temporal_client


async def close_temporal_client() -> None:
    """Close Temporal client connection.

    This function should be called during application shutdown.
    """
    global _temporal_client

    if _temporal_client is not None:
        try:
            await _temporal_client.close()
            logger.info("Temporal client connection closed")
        except Exception as e:
            logger.error(f"Error closing Temporal client: {e}")
        finally:
            _temporal_client = None
