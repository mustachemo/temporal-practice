"""Temporal worker for executing workflows and activities."""

# ================================== Imports ================================== #
# Standard Library
import asyncio
import os
from typing import Any

# Third-party
from temporalio.client import Client
from temporalio.worker import Worker, UnsandboxedWorkflowRunner
from omegaconf import DictConfig
from loguru import logger

# Local Application
from src.workflows.simple_workflow import (
    SimpleWorkflow,
    validate_input_activity,
    process_data_activity,
    store_data_activity,
)


# ================================== Functions ================================ #
async def start_temporal_worker(cfg: DictConfig) -> None:
    """Start the Temporal worker.

    Args:
        cfg: Hydra configuration object.
    """
    try:
        logger.info("Starting Temporal worker")

        # Connect to Temporal server
        temporal_address = os.getenv(
            "TEMPORAL_HOST", f"{cfg.temporal.server.host}:{cfg.temporal.server.port}"
        )
        client = await Client.connect(
            temporal_address,
            namespace=cfg.temporal.server.namespace,
        )

        # Create worker
        worker = Worker(
            client,
            task_queue=cfg.temporal.worker.task_queue,
            workflows=[SimpleWorkflow],
            activities=[
                validate_input_activity,
                process_data_activity,
                store_data_activity,
            ],
            max_concurrent_activities=cfg.temporal.worker.max_concurrent_activities,
            workflow_runner=UnsandboxedWorkflowRunner(),
        )

        logger.info("Temporal worker configured and starting")

        # Start worker (this will run indefinitely)
        await worker.run()

    except Exception as e:
        logger.error(f"Failed to start Temporal worker: {e}")
        raise


async def run_worker_standalone(cfg: DictConfig) -> None:
    """Run the Temporal worker as a standalone process.

    Args:
        cfg: Hydra configuration object.
    """
    try:
        await start_temporal_worker(cfg)
    except KeyboardInterrupt:
        logger.info("Temporal worker stopped by user")
    except Exception as e:
        logger.error(f"Temporal worker failed: {e}")
        raise
