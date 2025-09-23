"""Pytest configuration and fixtures."""

# ================================== Imports ================================== #
# Standard Library
import asyncio
from typing import AsyncGenerator, Generator

# Third-party
import pytest
from fastapi.testclient import TestClient
from omegaconf import OmegaConf

# Local Application
from src.api.main import create_app

# ================================== Fixtures ================================= #
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def test_config() -> OmegaConf:
    """Get test configuration."""
    return OmegaConf.create({
        "app": {
            "name": "test-app",
            "version": "1.0.0",
            "debug": True
        },
        "temporal": {
            "server": {
                "host": "localhost",
                "port": 7233,
                "namespace": "test"
            },
            "worker": {
                "task_queue": "test-task-queue",
                "max_concurrent_activities": 5,
                "max_concurrent_workflows": 5
            }
        },
        "database": {
            "url": "sqlite:///test.db",
            "pool_size": 5
        },
        "logging": {
            "level": "DEBUG"
        },
        "api": {
            "title": "Test API",
            "description": "Test API Description",
            "version": "1.0.0",
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "reload": False,
                "workers": 1
            },
            "cors": {
                "allow_origins": ["*"],
                "allow_credentials": True,
                "allow_methods": ["*"],
                "allow_headers": ["*"]
            },
            "docs": {
                "enabled": True,
                "path": "/docs",
                "redoc_path": "/redoc",
                "openapi_path": "/openapi.json"
            }
        }
    })

@pytest.fixture
def fastapi_client(test_config: OmegaConf) -> TestClient:
    """Create FastAPI test client."""
    app = create_app(test_config)
    return TestClient(app)
