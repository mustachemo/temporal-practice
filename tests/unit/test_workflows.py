"""Unit tests for workflow functionality."""

# ================================== Imports ================================== #
# Standard Library
from unittest.mock import patch, AsyncMock

# Third-party
import pytest

# Local Application
from src.models.workflow import WorkflowInput, WorkflowResult
from src.workflows.simple_workflow import (
    SimpleWorkflow,
    validate_input_activity,
    process_data_activity,
    store_data_activity,
)


# ================================== Test Classes ============================= #
class TestSimpleWorkflow:
    """Test cases for SimpleWorkflow."""

    def test_workflow_input_validation(self):
        """Test WorkflowInput model validation."""
        # Valid input
        valid_input = WorkflowInput(
            request_id="test-123",
            user_id="user-456",
            parameters={"required_field": "test_value"},
        )
        assert valid_input.request_id == "test-123"
        assert valid_input.user_id == "user-456"
        assert valid_input.parameters["required_field"] == "test_value"

    def test_workflow_result_creation(self):
        """Test WorkflowResult model creation."""
        # Success result
        success_result = WorkflowResult(
            success=True, result_data={"key": "value"}, execution_time=1.5
        )
        assert success_result.success is True
        assert success_result.result_data["key"] == "value"
        assert success_result.execution_time == 1.5

        # Failure result
        failure_result = WorkflowResult(success=False, error_message="Test error")
        assert failure_result.success is False
        assert failure_result.error_message == "Test error"
        assert failure_result.result_data is None


class TestWorkflowActivities:
    """Test cases for workflow activities."""

    @pytest.mark.asyncio
    async def test_validate_input_activity_success(self):
        """Test successful input validation."""
        parameters = {"required_field": "test_value"}
        result = await validate_input_activity(parameters)

        assert result["valid"] is True
        assert "successful" in result["message"]

    @pytest.mark.asyncio
    async def test_validate_input_activity_failure(self):
        """Test input validation failure."""
        parameters = {}
        result = await validate_input_activity(parameters)

        assert result["valid"] is False
        assert "No parameters provided" in result["message"]

    @pytest.mark.asyncio
    async def test_validate_input_activity_missing_field(self):
        """Test input validation with missing required field."""
        parameters = {"other_field": "value"}
        result = await validate_input_activity(parameters)

        assert result["valid"] is False
        assert "Missing required field" in result["message"]

    @pytest.mark.asyncio
    async def test_process_data_activity(self):
        """Test data processing activity."""
        parameters = {"required_field": "test_value"}
        result = await process_data_activity(parameters)

        assert result["processed"] is True
        assert "data" in result
        assert result["data"]["original"] == parameters
        assert result["data"]["processed_value"] == "TEST_VALUE"

    @pytest.mark.asyncio
    async def test_store_data_activity(self):
        """Test data storage activity."""
        processed_data = {"processed": True, "data": {"key": "value"}}
        result = await store_data_activity(processed_data)

        assert result["stored"] is True
        assert "storage_id" in result
        assert "Data stored successfully" in result["message"]
