"""Simple workflow demonstrating basic Temporal patterns."""

# ================================== Imports ================================== #
# Standard Library
from datetime import timedelta
from typing import Any, Dict

# Third-party
from temporalio import workflow, activity
from loguru import logger

# Local Application
from src.models.workflow import WorkflowInput, WorkflowResult


# ================================== Workflow Definition ===================== #
@workflow.defn
class SimpleWorkflow:
    """Simple workflow demonstrating basic Temporal patterns."""

    def __init__(self) -> None:
        self.logger = workflow.logger()

    @workflow.run
    async def run(self, input_data: WorkflowInput) -> WorkflowResult:
        """Main workflow execution method.

        Args:
            input_data: Input data for the workflow.

        Returns:
            Workflow result with success status and data.
        """
        try:
            self.logger.info(
                f"Starting simple workflow for request {input_data.request_id}"
            )

            # Execute workflow steps
            result = await self._execute_workflow_steps(input_data)

            self.logger.info(
                f"Simple workflow completed successfully for {input_data.request_id}"
            )
            return WorkflowResult(success=True, result_data=result)

        except Exception as e:
            self.logger.error(
                f"Simple workflow failed for {input_data.request_id}: {e}"
            )
            return WorkflowResult(success=False, error_message=str(e))

    async def _execute_workflow_steps(
        self, input_data: WorkflowInput
    ) -> Dict[str, Any]:
        """Execute the main workflow logic.

        Args:
            input_data: Input data for the workflow.

        Returns:
            Dictionary containing workflow results.
        """
        # Step 1: Validate input
        validation_result = await workflow.execute_activity(
            validate_input_activity,
            input_data.parameters,
            start_to_close_timeout=timedelta(minutes=2),
        )

        if not validation_result.get("valid", False):
            raise ValueError(
                f"Input validation failed: {validation_result.get('message', 'Unknown error')}"
            )

        # Step 2: Process data
        processing_result = await workflow.execute_activity(
            process_data_activity,
            input_data.parameters,
            start_to_close_timeout=timedelta(minutes=5),
        )

        # Step 3: Store results
        storage_result = await workflow.execute_activity(
            store_data_activity,
            processing_result,
            start_to_close_timeout=timedelta(minutes=3),
        )

        return {
            "validation": validation_result,
            "processing": processing_result,
            "storage": storage_result,
            "workflow_id": input_data.request_id,
            "user_id": input_data.user_id,
        }


# ================================== Activities =============================== #
@activity.defn
async def validate_input_activity(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Validate input parameters.

    Args:
        parameters: Input parameters to validate.

    Returns:
        Validation result dictionary.
    """
    logger.info("Validating input parameters")

    # Simple validation logic
    if not parameters:
        return {"valid": False, "message": "No parameters provided"}

    if "required_field" not in parameters:
        return {"valid": False, "message": "Missing required field"}

    return {"valid": True, "message": "Input validation successful"}


@activity.defn
async def process_data_activity(parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Process input data.

    Args:
        parameters: Input parameters to process.

    Returns:
        Processing result dictionary.
    """
    logger.info("Processing data")

    # Simulate some processing
    from datetime import datetime, timezone

    processed_data = {
        "original": parameters,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "processed_value": parameters.get("required_field", "").upper(),
    }

    return {"processed": True, "data": processed_data}


@activity.defn
async def store_data_activity(processed_data: Dict[str, Any]) -> Dict[str, Any]:
    """Store processed data.

    Args:
        processed_data: Processed data to store.

    Returns:
        Storage result dictionary.
    """
    logger.info("Storing processed data")

    # Simulate storage
    from datetime import datetime, timezone

    storage_id = f"storage_{datetime.now(timezone.utc).timestamp()}"

    return {
        "stored": True,
        "storage_id": storage_id,
        "message": "Data stored successfully",
    }
