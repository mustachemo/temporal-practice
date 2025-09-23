"""FastAPI application creation and configuration."""

# ================================== Imports ================================== #
# Standard Library
from contextlib import asynccontextmanager
from typing import Any

# Third-party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from omegaconf import DictConfig
from loguru import logger

# Local Application
from src.api.routes import workflows, health
from src.models.workflow import ErrorResponse


# ================================== Functions ================================ #
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("FastAPI application started")
    yield
    # Shutdown
    logger.info("FastAPI application shutting down")


def create_app(cfg: DictConfig) -> FastAPI:
    """Create and configure the FastAPI application.

    Args:
        cfg: Hydra configuration object.

    Returns:
        Configured FastAPI application instance.
    """
    # Create FastAPI app
    app = FastAPI(
        title=cfg.api.title,
        description=cfg.api.description,
        version=cfg.api.version,
        docs_url=cfg.api.docs.path if cfg.api.docs.enabled else None,
        redoc_url=cfg.api.docs.redoc_path if cfg.api.docs.enabled else None,
        openapi_url=cfg.api.docs.openapi_path if cfg.api.docs.enabled else None,
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cfg.api.cors.allow_origins,
        allow_credentials=cfg.api.cors.allow_credentials,
        allow_methods=cfg.api.cors.allow_methods,
        allow_headers=cfg.api.cors.allow_headers,
    )

    # Add exception handlers
    setup_exception_handlers(app)

    # Include routers
    app.include_router(workflows.router, prefix="/api/v1")
    app.include_router(health.router, prefix="/api/v1")

    return app


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup global exception handlers for the application.

    Args:
        app: FastAPI application instance.
    """
    from fastapi import HTTPException

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Any, exc: HTTPException) -> JSONResponse:
        """Handle HTTP exceptions with consistent error format."""
        logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="HTTP_ERROR",
                message=exc.detail,
                details={"status_code": exc.status_code},
            ).dict(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Any, exc: Exception) -> JSONResponse:
        """Handle unexpected exceptions."""
        logger.error("Unexpected error: {}", exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="INTERNAL_ERROR",
                message="An unexpected error occurred",
                details={"exception_type": type(exc).__name__},
            ).dict(),
        )
