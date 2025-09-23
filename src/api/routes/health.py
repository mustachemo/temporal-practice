"""Health check API routes."""

# ================================== Imports ================================== #
# Standard Library
from datetime import datetime, timezone
from typing import Dict, Any

# Third-party
from fastapi import APIRouter, HTTPException
from loguru import logger

# ================================== Router Setup ============================= #
router = APIRouter(prefix="/health", tags=["health"])


# ================================== Routes =================================== #
@router.get("/")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint.

    Returns:
        Basic health status information.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "temporal-workflow-service",
    }


@router.get("/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check with metrics.

    Returns:
        Detailed health status with system metrics.

    Raises:
        HTTPException: If service is unhealthy.
    """
    try:
        # Check system health
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": "temporal-workflow-service",
            "version": "1.0.0",
            "checks": {
                "temporal_connection": await _check_temporal_connection(),
                "database_connection": await _check_database_connection(),
                "redis_connection": await _check_redis_connection(),
            },
        }

        # Determine overall health
        all_checks_healthy = all(
            check["status"] == "healthy" for check in health_status["checks"].values()
        )

        if not all_checks_healthy:
            health_status["status"] = "unhealthy"

        return health_status

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


# ================================== Helper Functions ========================= #
async def _check_temporal_connection() -> Dict[str, str]:
    """Check Temporal server connection.

    Returns:
        Connection status information.
    """
    try:
        # TODO: Implement actual connection check
        return {"status": "healthy", "message": "Temporal connection OK"}
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}


async def _check_database_connection() -> Dict[str, str]:
    """Check database connection.

    Returns:
        Connection status information.
    """
    try:
        # TODO: Implement actual connection check
        return {"status": "healthy", "message": "Database connection OK"}
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}


async def _check_redis_connection() -> Dict[str, str]:
    """Check Redis connection.

    Returns:
        Connection status information.
    """
    try:
        # TODO: Implement actual connection check
        return {"status": "healthy", "message": "Redis connection OK"}
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}
