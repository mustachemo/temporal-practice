"""Main application entry point with Hydra configuration."""

# ================================== Imports ================================== #
# Standard Library
import asyncio
from pathlib import Path

# Third-party
import hydra
from omegaconf import DictConfig, OmegaConf
import logging

# Local Application
from src.api.main import create_app
from src.workers.temporal_worker import start_temporal_worker


# ================================== Functions ================================ #
@hydra.main(config_path="/app/conf/config", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    """Main function orchestrated by Hydra.

    Args:
        cfg: The configuration object populated by Hydra.
    """
    # -------------------------- Initialization -------------------------- #
    logging.basicConfig(level=logging.INFO)
    logging.getLogger(__name__).info(
        f"Starting {cfg.app.name if 'app' in cfg else cfg.app_name} v{cfg.app.version if 'app' in cfg else cfg.version}"
    )
    logging.getLogger(__name__).debug(f"Configuration:\n{OmegaConf.to_yaml(cfg)}")

    # -------------------------- Core Logic ------------------------------ #
    try:
        # Create FastAPI app
        app = create_app(cfg)

        # Note: Temporal worker should be run separately

        # Start FastAPI server
        import uvicorn

        uvicorn.run(
            app,
            host=cfg.api.server.host,
            port=cfg.api.server.port,
            workers=cfg.api.server.workers,
            reload=cfg.api.server.reload,
            log_config=None,  # Use our custom logging
        )

    except Exception as e:
        logging.getLogger(__name__).exception("Application startup failed")
        raise


if __name__ == "__main__":
    main()
