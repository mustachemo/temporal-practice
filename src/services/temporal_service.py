"""Temporal service for workflow management."""

# ================================== Imports ================================== #
# Standard Library
from typing import Optional

# Third-party
from temporalio.client import Client
from loguru import logger

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
            # TODO: Get connection details from configuration
            _temporal_client = await Client.connect("localhost:7233")
            logger.info("Connected to Temporal server")
        except Exception as e:
            logger.error(f"Failed to connect to Temporal server: {e}")
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
