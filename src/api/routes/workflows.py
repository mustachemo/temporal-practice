"""Workflow management API routes."""

# ================================== Imports ================================== #
# Standard Library
from datetime import datetime
from typing import Any, Dict

# Third-party
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from temporalio.client import Client
import logging

# Local Application
from src.models.workflow import (
    WorkflowRequest,
    WorkflowResponse,
    WorkflowStatus,
    ErrorResponse,
)
from src.services.temporal_service import get_temporal_client
from src.workflows.simple_workflow import SimpleWorkflow

# ================================== Router Setup ============================= #
router = APIRouter(prefix="/workflows", tags=["workflows"])


# ================================== Routes =================================== #
@router.post("/start", response_model=WorkflowResponse)
async def start_workflow(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks,
    client: Client = Depends(get_temporal_client),
) -> WorkflowResponse:
    """Start a new workflow instance.

    Args:
        request: Workflow start request data.
        background_tasks: FastAPI background tasks.
        client: Temporal client instance.

    Returns:
        Workflow response with workflow ID and status.

    Raises:
        HTTPException: If workflow start fails.
    """
    try:
        logging.getLogger(__name__).info(
            f"Starting workflow: {request.workflow_type} for user {request.user_id}"
        )

        # Start workflow asynchronously
        # Map workflow type string to actual workflow class
        workflow_class = SimpleWorkflow  # For now, only support SimpleWorkflow

        # Create WorkflowInput object from request data
        from src.models.workflow import WorkflowInput
        workflow_input = WorkflowInput(
            request_id=f"{request.workflow_type}_{request.user_id}_{datetime.now().timestamp()}",
            user_id=request.user_id,
            parameters=request.input_data,
        )

        workflow_handle = await client.start_workflow(
            workflow_class,
            args=[workflow_input],
            id=f"{request.workflow_type}_{request.user_id}_{datetime.now().timestamp()}",
            task_queue="workflow-task-queue",
        )

        # Add cleanup task to background
        background_tasks.add_task(
            _log_workflow_start, workflow_handle.id, request.workflow_type
        )

        return WorkflowResponse(
            workflow_id=workflow_handle.id,
            status="STARTED",
            message="Workflow started successfully",
            created_at=datetime.now().isoformat(),
        )

    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to start workflow: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to start workflow: {str(e)}"
        )


@router.get("/{workflow_id}/status", response_model=WorkflowResponse)
async def get_workflow_status(
    workflow_id: str, client: Client = Depends(get_temporal_client)
) -> WorkflowResponse:
    """Get the current status of a workflow.

    Args:
        workflow_id: Unique identifier for the workflow.
        client: Temporal client instance.

    Returns:
        Workflow response with current status.

    Raises:
        HTTPException: If workflow is not found.
    """
    try:
        workflow_handle = client.get_workflow_handle(workflow_id)
        status = await workflow_handle.describe()

        return WorkflowResponse(
            workflow_id=workflow_id,
            status=status.status.name,
            message=f"Workflow is {status.status.name.lower()}",
            created_at=status.start_time.isoformat(),
        )

    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to get workflow status: {e}")
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")


@router.post("/{workflow_id}/signal")
async def signal_workflow(
    workflow_id: str,
    signal_data: Dict[str, Any],
    client: Client = Depends(get_temporal_client),
) -> Dict[str, str]:
    """Send a signal to a running workflow.

    Args:
        workflow_id: Unique identifier for the workflow.
        signal_data: Signal data to send.
        client: Temporal client instance.

    Returns:
        Success message.

    Raises:
        HTTPException: If signal sending fails.
    """
    try:
        workflow_handle = client.get_workflow_handle(workflow_id)
        await workflow_handle.signal("workflow_signal", signal_data)

        return {"message": "Signal sent successfully"}

    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to send signal: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send signal: {str(e)}")


@router.get("/{workflow_id}/result")
async def get_workflow_result(
    workflow_id: str, client: Client = Depends(get_temporal_client)
) -> Dict[str, Any]:
    """Get the result of a completed workflow.

    Args:
        workflow_id: Unique identifier for the workflow.
        client: Temporal client instance.

    Returns:
        Workflow result data.

    Raises:
        HTTPException: If workflow result retrieval fails.
    """
    try:
        workflow_handle = client.get_workflow_handle(workflow_id)
        result = await workflow_handle.result()

        return {"workflow_id": workflow_id, "result": result, "status": "COMPLETED"}

    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to get workflow result: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get workflow result: {str(e)}"
        )


# ================================== Helper Functions ========================= #
async def _log_workflow_start(workflow_id: str, workflow_type: str) -> None:
    """Log workflow start in background.

    Args:
        workflow_id: Unique identifier for the workflow.
        workflow_type: Type of workflow being started.
    """
    logging.getLogger(__name__).info(f"Workflow {workflow_id} of type {workflow_type} started")
