"""Unit tests for API functionality."""

# ================================== Imports ================================== #
# Standard Library
from unittest.mock import patch, AsyncMock

# Third-party
import pytest
from fastapi.testclient import TestClient

# Local Application
from src.models.workflow import WorkflowRequest


# ================================== Test Classes ============================= #
class TestWorkflowAPI:
    """Test cases for workflow API endpoints."""

    def test_health_check(self, fastapi_client: TestClient):
        """Test basic health check endpoint."""
        response = fastapi_client.get("/api/v1/health/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["service"] == "temporal-workflow-service"

    def test_detailed_health_check(self, fastapi_client: TestClient):
        """Test detailed health check endpoint."""
        response = fastapi_client.get("/api/v1/health/detailed")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "checks" in data
        assert "temporal_connection" in data["checks"]
        assert "database_connection" in data["checks"]
        assert "redis_connection" in data["checks"]

    @patch("src.services.temporal_service.get_temporal_client")
    def test_start_workflow_success(self, mock_get_client, fastapi_client: TestClient):
        """Test successful workflow start."""
        # Mock Temporal client
        mock_client = AsyncMock()
        mock_workflow_handle = AsyncMock()
        mock_workflow_handle.id = "test-workflow-123"
        mock_client.start_workflow.return_value = mock_workflow_handle
        mock_get_client.return_value = mock_client

        # Test data
        request_data = {
            "workflow_type": "simple_workflow",
            "input_data": {"required_field": "test_value"},
            "user_id": "test_user",
        }

        response = fastapi_client.post("/api/v1/workflows/start", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["workflow_id"] == "test-workflow-123"
        assert data["status"] == "STARTED"
        assert "message" in data

    def test_start_workflow_validation_error(self, fastapi_client: TestClient):
        """Test workflow start with validation error."""
        # Invalid request data
        request_data = {
            "workflow_type": "",  # Empty workflow type
            "input_data": {"test": "data"},
            "user_id": "test_user",
        }

        response = fastapi_client.post("/api/v1/workflows/start", json=request_data)

        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "error" in data

    @patch("src.services.temporal_service.get_temporal_client")
    def test_get_workflow_status_success(
        self, mock_get_client, fastapi_client: TestClient
    ):
        """Test getting workflow status."""
        # Mock Temporal client
        mock_client = AsyncMock()
        mock_workflow_handle = AsyncMock()
        mock_status = AsyncMock()
        mock_status.status.name = "RUNNING"
        mock_status.start_time.isoformat.return_value = "2023-01-01T00:00:00"

        mock_workflow_handle.describe.return_value = mock_status
        mock_client.get_workflow_handle.return_value = mock_workflow_handle
        mock_get_client.return_value = mock_client

        workflow_id = "test-workflow-123"
        response = fastapi_client.get(f"/api/v1/workflows/{workflow_id}/status")

        assert response.status_code == 200
        data = response.json()
        assert data["workflow_id"] == workflow_id
        assert data["status"] == "RUNNING"
        assert "message" in data

    @patch("src.services.temporal_service.get_temporal_client")
    def test_get_workflow_status_not_found(
        self, mock_get_client, fastapi_client: TestClient
    ):
        """Test getting status of non-existent workflow."""
        # Mock Temporal client to raise exception
        mock_client = AsyncMock()
        mock_client.get_workflow_handle.side_effect = Exception("Workflow not found")
        mock_get_client.return_value = mock_client

        workflow_id = "non-existent-workflow"
        response = fastapi_client.get(f"/api/v1/workflows/{workflow_id}/status")

        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "not found" in data["message"].lower()

    @patch("src.services.temporal_service.get_temporal_client")
    def test_signal_workflow_success(self, mock_get_client, fastapi_client: TestClient):
        """Test sending signal to workflow."""
        # Mock Temporal client
        mock_client = AsyncMock()
        mock_workflow_handle = AsyncMock()
        mock_client.get_workflow_handle.return_value = mock_workflow_handle
        mock_get_client.return_value = mock_client

        workflow_id = "test-workflow-123"
        signal_data = {"signal_type": "pause", "reason": "maintenance"}

        response = fastapi_client.post(
            f"/api/v1/workflows/{workflow_id}/signal", json=signal_data
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data

        # Verify signal was sent
        mock_workflow_handle.signal.assert_called_once_with(
            "workflow_signal", signal_data
        )

    @patch("src.services.temporal_service.get_temporal_client")
    def test_get_workflow_result_success(
        self, mock_get_client, fastapi_client: TestClient
    ):
        """Test getting workflow result."""
        # Mock Temporal client
        mock_client = AsyncMock()
        mock_workflow_handle = AsyncMock()
        mock_result = {"success": True, "data": "test_result"}
        mock_workflow_handle.result.return_value = mock_result
        mock_client.get_workflow_handle.return_value = mock_workflow_handle
        mock_get_client.return_value = mock_client

        workflow_id = "test-workflow-123"
        response = fastapi_client.get(f"/api/v1/workflows/{workflow_id}/result")

        assert response.status_code == 200
        data = response.json()
        assert data["workflow_id"] == workflow_id
        assert data["result"] == mock_result
        assert data["status"] == "COMPLETED"
