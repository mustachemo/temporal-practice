"""Script to run the Temporal worker as a standalone process."""

# ================================== Imports ================================== #
# Standard Library
import asyncio

# Third-party
import hydra
from omegaconf import DictConfig
import logging

# Local Application
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.workers.temporal_worker import run_worker_standalone


# ================================== Functions ================================ #
@hydra.main(config_path="/app/conf/config", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    """Main function to run the Temporal worker.

    Args:
        cfg: Hydra configuration object.
    """
    # Setup basic logging for worker process
    logging.basicConfig(level=logging.INFO)

    logging.getLogger(__name__).info("Starting Temporal worker process")

    # Run the worker
    asyncio.run(run_worker_standalone(cfg))


if __name__ == "__main__":
    main()
