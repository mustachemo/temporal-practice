"""Main application entry point with Hydra configuration."""

# ================================== Imports ================================== #
# Standard Library
import asyncio
from pathlib import Path

# Third-party
import hydra
from loguru import logger
from omegaconf import DictConfig, OmegaConf
from rich.console import Console

# Local Application
from src.api.main import create_app
from src.utils.logging import setup_logger
from src.workers.temporal_worker import start_temporal_worker

# ================================== Functions ================================ #
@hydra.main(config_path="../conf", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    """Main function orchestrated by Hydra.

    Args:
        cfg: The configuration object populated by Hydra.
    """
    # -------------------------- Initialization -------------------------- #
    console = Console()
    setup_logger(Path("logs/app.log"))
    
    logger.info(f"Starting [bold cyan]{cfg.app_name}[/bold cyan] v{cfg.version}")
    logger.debug(f"Configuration:\n{OmegaConf.to_yaml(cfg)}")

    # -------------------------- Core Logic ------------------------------ #
    try:
        # Create FastAPI app
        app = create_app(cfg)
        
        # Start Temporal worker in background
        asyncio.create_task(start_temporal_worker(cfg))
        
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
        logger.opt(exception=True).critical("Application startup failed.")
        console.print("[bold red]A critical error occurred. Check the logs for details.[/bold red]")
        raise

if __name__ == "__main__":
    main()
