"""Script to run the Temporal worker as a standalone process."""

# ================================== Imports ================================== #
# Standard Library
import asyncio

# Third-party
import hydra
from omegaconf import DictConfig
from loguru import logger

# Local Application
from src.workers.temporal_worker import run_worker_standalone
from src.utils.logging import setup_logger


# ================================== Functions ================================ #
@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    """Main function to run the Temporal worker.

    Args:
        cfg: Hydra configuration object.
    """
    # Setup logging
    setup_logger()

    logger.info("Starting Temporal worker process")

    # Run the worker
    asyncio.run(run_worker_standalone(cfg))


if __name__ == "__main__":
    main()
