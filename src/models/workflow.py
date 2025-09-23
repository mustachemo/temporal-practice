"""Workflow-related data models."""

# ================================== Imports ================================== #
# Standard Library
from datetime import datetime
from typing import Any, Dict, Optional

# Third-party
from pydantic import BaseModel, Field


# ================================== Data Models ============================= #
class WorkflowRequest(BaseModel):
    """Request model for starting a workflow."""

    workflow_type: str = Field(..., description="Type of workflow to execute")
    input_data: Dict[str, Any] = Field(..., description="Input data for the workflow")
    user_id: str = Field(..., description="ID of the user initiating the workflow")

    class Config:
        schema_extra = {
            "example": {
                "workflow_type": "data_processing",
                "input_data": {"file_path": "/path/to/file", "options": {}},
                "user_id": "user_123",
            }
        }


class WorkflowResponse(BaseModel):
    """Response model for workflow operations."""

    workflow_id: str = Field(..., description="Unique identifier for the workflow")
    status: str = Field(..., description="Current status of the workflow")
    message: str = Field(..., description="Human-readable message")
    created_at: str = Field(..., description="ISO timestamp when workflow was created")


class WorkflowStatus(BaseModel):
    """Model for workflow status information."""

    workflow_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    execution_time: Optional[float] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class WorkflowInput(BaseModel):
    """Input data structure for workflows."""

    request_id: str = Field(..., description="Unique request identifier")
    user_id: str = Field(..., description="User initiating the workflow")
    parameters: Dict[str, Any] = Field(..., description="Workflow parameters")
    correlation_id: Optional[str] = Field(
        None, description="Correlation ID for tracing"
    )


class WorkflowResult(BaseModel):
    """Output data structure for workflows."""

    success: bool = Field(..., description="Whether the workflow succeeded")
    result_data: Optional[Dict[str, Any]] = Field(
        None, description="Workflow result data"
    )
    error_message: Optional[str] = Field(None, description="Error message if failed")
    execution_time: Optional[float] = Field(
        None, description="Total execution time in seconds"
    )


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional error details"
    )
