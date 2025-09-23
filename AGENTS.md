write me an example code in markdown with ```python``` so that I can tell the agent how to behave, make sure it follows the best practices and instructions outlined below:

### Guiding Principles

The primary goal is to produce code that is **clear, robust, maintainable, and Pythonic**.
* **Clarity over cleverness**: Write code that is easy to understand.
* **Self-documenting**: Strive for descriptive names and logical structure that minimizes the need for explanatory comments.
* **Robustness**: Anticipate and handle potential errors gracefully.


### Assistant Behavior
* If I tell you that you are wrong, re-evaluate your response based on the facts provided.
* Avoid apologies or conciliatory statements like "You're right" or "Yes."
* Stick to the task at hand. Avoid hyperbole and unnecessary conversational filler.
* Ensure responses are relevant to the provided context and code. Keep them concise.
* Think step-by-step to validate your reasoning before responding.
* For each code snippet, provide a brief explanation of the changes made and why they improve the code.
* When suggesting code, ensure it adheres to the guidelines below.
* When refactoring, ensure existing functionality is preserved unless explicitly instructed otherwise.
* When adding new features, ensure they integrate seamlessly with existing code and follow the same style and conventions.
* When correcting errors, provide a clear explanation of the issue and how the fix addresses it.
* Always prioritize best practices and modern Python idioms.
* When suggesting libraries or tools, prefer widely adopted and well-maintained options.
* When dealing with performance optimizations, ensure that changes do not compromise code readability or maintainability unless absolutely necessary.
* When working with asynchronous code, ensure proper use of `async`/`await` and avoid blocking operations.
* When working with type hints, ensure they are accurate and comprehensive, covering all function signatures and complex data structures.
* When working with data structures, prefer built-in types and standard library collections unless a third-party library offers significant advantages.

---

### Style & Formatting

#### Naming Conventions
* **Variables & Functions**: Use descriptive, `snake_case` names. Avoid unclear abbreviations. Domain-specific abbreviations like `img` (image), `rso` (Resident Space Object), and `bg` (background) are acceptable if they enhance readability.
* **Constants**: Use `ALL_CAPS_SNAKE_CASE` (Screaming Snake Case).

#### Code Structure
* **Indentation**: Use 4 spaces per indentation level.
* **Nesting**: Avoid deeply nested logic. Decompose complex blocks into smaller, more focused functions.
* **Line Length**: Keep lines under 120 characters to align with modern standards.
* **Imports**: Group imports in the following order: standard library, third-party packages, and local application/library specific imports. Sort each group alphabetically.
* **Section Separators**: Use a consistent comment style to break up large files into logical sections.
    ```python
    # =============================== Constants/Functions ================================= #
    # --------------------------------- Complex Logic -------------------------------- #
    ```

---

### Documentation & Comments

#### Docstrings
* All classes, functions, and methods must have a docstring that follows the **Google Python Style Guide**.
* Use triple double-quotes (`"""Docstring content..."""`). The summary line should be on the same line as the opening quotes.
* Include `Args:`, `Returns:`, and `Raises:` sections where applicable.

#### Inline & Block Comments
* Use inline comments sparingly, only to clarify complex or non-obvious logic.
* Employ the "Better Comments" style for annotations to improve readability:
    ```python
    # * Very important information is highlighted.
    # ? This is a question or clarification needed.
    # ! This is a warning or something to be cautious about.
    # TODO: This is a task that needs to be completed.
    ```


### Architecture Decisions
* For significant design choices (e.g., choosing a specific library, designing a core algorithm), add a brief document in a `docs/` directory. This provides context for future developers on *why* a decision was made.

### Designs
* Use `mermaid` syntax for diagrams in Markdown files to visualize architecture, workflows, or data flows.


---

### Code Patterns

#### Error Handling
* Handle exceptions specifically (e.g., `try...except FileNotFoundError`). Avoid catching generic `Exception` unless it's a last resort and is re-raised or logged with context.
* Use `try...except` blocks only for code where exceptions are expected and can be handled meaningfully. Do not use them for regular control flow.

#### Type Hinting
* All function and method signatures, as well as variable declarations where appropriate, must include type hints using standard types such as 'int', 'float', 'str', 'bool', 'list', 'dict', and 'tuple' and the `typing` module when necessary (e.g., when using `Optional`).

#### Language Features
* **File Paths**: Use the `pathlib` module for all filesystem path manipulations to ensure cross-platform compatibility.
* **Configuration**: Avoid magic strings and numbers. Define them as constants or parameterize them.
* **String Formatting**: Use f-strings (`f"..."`) for all string formatting.
* **Yields**: Use `yield` for generators when returning a sequence of items, especially in I/O-bound operations.

---
### Testing

Code is not complete until it is tested. Tests are critical for ensuring correctness, preventing regressions, and enabling confident refactoring.

#### Framework & Tooling

  * **Framework**: Use `pytest` as the primary testing framework. Its use of plain `assert` statements and its powerful fixture system make it superior for most use cases.
  * **Test Runner**: Run tests using the `pytest` command.
  * **Test Coverage**: Use the `pytest-cov` plugin to measure test coverage. While 100% coverage is not always the goal, it is a useful metric for identifying untested code paths.
  * **Mocking**: Use `pytest-mock` (which wraps `unittest.mock`) for mocking dependencies and isolating units of code.
  * **CLI Testing**: For `typer` applications, use `typer.testing.CliRunner` to invoke commands and assert their output, exit codes, and side effects.

#### Test Structure

  * **Directory**: All tests must reside in a top-level `tests/` directory.
  * **File Naming**: Test files must be named `test_*.py`.
  * **Directory Mirroring**: The structure of the `tests/` directory should mirror the application's source directory to make tests easy to locate.
    ```
    project/
    ├── src/
    │   └── my_module/
    │       ├── __init__.py
    │       └── processing.py
    └── tests/
        └── my_module/
            └── test_processing.py
    ```

#### Best Practices

  * **Arrange-Act-Assert (AAA)**: Structure tests using the AAA pattern for clarity.
    1.  **Arrange**: Set up the initial state and inputs.
    2.  **Act**: Execute the function or method being tested.
    3.  **Assert**: Verify that the outcome is as expected.
  * **Fixtures**: Use `pytest` fixtures (`@pytest.fixture`) to provide a fixed baseline for tests, such as creating temporary directories, database connections, or complex objects. This promotes reusability and reduces boilerplate.
  * **Independence**: Tests must be independent and produce the same result regardless of the order in which they are run. Do not rely on side effects from previous tests.
  * **Specificity**: Unit tests should be focused, testing one piece of logic at a time. Integration tests can verify the interaction between multiple components.

---

### Recommended Libraries
* **Numerical Operations**: `numpy`
* **File Paths**: `pathlib`
* **CLI Applications**: `typer` (where applicable)
* **Console Output**: `rich`
* **Logging**: `loguru` (for advanced logging capabilities)
* **dataclasses**: Use `dataclasses` for simple data structures to improve readability and maintainability.
* **itertools**: Use `itertools` for efficient looping and combinatorial operations.
* **collections**: Use `collections` for specialized data structures like `defaultdict`, `Counter`, and `namedtuple`.
* **concurrent.futures**: Use `concurrent.futures` for parallel execution of tasks. Use `ThreadPoolExecutor` for I/O-bound tasks and `ProcessPoolExecutor` for CPU-bound tasks.

---

### Python Example Code

#### Logging Utility

```python
# ================================== Imports ================================== #
# Standard Library
import sys
from pathlib import Path

# Third-party
from loguru import logger
from rich.logging import RichHandler

# ================================== Functions ================================ #
def setup_logger(log_file: Path) -> None:
    """Configures Loguru to provide rich console logging and file logging.

    This setup ensures that logs are easy to read during interactive runs
    and are persistently stored for debugging and auditing purposes.

    Args:
        log_file: The file path to store logs.
    """
    # * Ensure the directory for the log file exists.
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger.remove() # Remove the default handler to avoid duplicate outputs.

    # Console logger with rich formatting
    logger.add(
        sys.stderr,
        level="INFO",
        format="{message}",
        enqueue=True, # Makes logging from multiple processes/threads safe.
        backtrace=True, # Show full stack trace on exceptions.
        colorize=True,
        handler=RichHandler(
            rich_tracebacks=True,
            show_path=False, # Cleaner output
            markup=True,
        ),
    )

    # File logger for persistence
    logger.add(
        log_file,
        level="DEBUG", # Log more detailed info to the file.
        rotation="10 MB", # Rotate the log file when it reaches 10 MB.
        retention="10 days",
        enqueue=True,
        backtrace=True,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}"
    )

    logger.info("[bold green]Logger configured successfully.[/bold green]")
```

#### Core Processing Logic
```python
# ================================== Imports ================================== #
# Standard Library
import csv
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party
from loguru import logger
from omegaconf import DictConfig
from rich.progress import Progress

# ================================== Constants ================================ #
SUCCESS_STATUS = "SUCCESS"
FAILURE_STATUS = "FAILURE"

# ================================= Dataclasses =============================== #
@dataclass(frozen=True)
class ImageMetadata:
    """Immutable data structure for image metadata."""
    image_id: str
    file_path: Path
    confidence_score: float
    rso_class: str

@dataclass
class ProcessingResult:
    """Mutable data structure for capturing the result of a single operation."""
    metadata: ImageMetadata
    status: str
    message: str = ""

# ============================== Processing Class ============================= #
class ImageProcessor:
    """Orchestrates the loading, filtering, and processing of image assets."""
    def __init__(self, cfg: DictConfig):
        """Initializes the processor with a Hydra configuration object.

        Args:
            cfg: The OmegaConf DictConfig object provided by Hydra.
        """
        self.cfg = cfg
        self.input_csv = Path(self.cfg.paths.input_csv)
        self.output_dir = Path(self.cfg.paths.output_dir)
        # * Create the output directory idempotently.
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory set to: '{self.output_dir.resolve()}'")

    def _load_and_filter_metadata(self) -> Iterator[ImageMetadata]:
        """Loads and yields ImageMetadata records meeting filter criteria.

        Uses a generator to remain memory-efficient on large CSV files.

        Yields:
            An iterator of ImageMetadata objects that match the filters.

        Raises:
            FileNotFoundError: If the input_csv path does not exist.
            KeyError: If the CSV is missing required columns.
            ValueError: If a row has an invalid confidence score format.
        """
        logger.info(f"Loading metadata from: '{self.input_csv}'")
        if not self.input_csv.is_file():
            raise FileNotFoundError(f"Input CSV not found at: {self.input_csv}")

        try:
            with self.input_csv.open(mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        confidence = float(row["confidence_score"])
                        if confidence < self.cfg.processing.min_confidence:
                            continue

                        required_class = self.cfg.processing.required_class
                        if required_class and row["rso_class"] != required_class:
                            continue

                        yield ImageMetadata(
                            image_id=row["image_id"],
                            file_path=Path(row["file_path"]),
                            confidence_score=confidence,
                            rso_class=row["rso_class"],
                        )
                    except (KeyError, ValueError) as e:
                        logger.warning(f"Skipping malformed row: {row}. Reason: {e}")
                        continue
        except Exception as e:
            logger.opt(exception=True).error(
                f"A critical error occurred while reading the CSV file."
            )
            raise e

    def _simulate_image_processing(self, metadata: ImageMetadata) -> ProcessingResult:
        """Simulates a single I/O-bound image processing task.

        In a real application, this would contain logic for copying, resizing,
        or augmenting an image file.

        Args:
            metadata: The metadata object for the image to be processed.

        Returns:
            A ProcessingResult indicating the outcome.
        """
        try:
            logger.debug(f"Processing image_id: {metadata.image_id}")
            # Simulate I/O work (e.g., network download, disk read/write).
            time.sleep(self.cfg.processing.simulate_io_delay_seconds)

            # ? In a real-world scenario, you would perform file operations here.
            # ? For example: shutil.copy(metadata.file_path, self.output_dir)
            if not metadata.file_path.name: # A trivial failure condition
                 raise ValueError("File path appears to be a directory.")

            return ProcessingResult(metadata=metadata, status=SUCCESS_STATUS)
        except Exception as e:
            logger.error(f"Failed to process {metadata.image_id}: {e}")
            return ProcessingResult(metadata=metadata, status=FAILURE_STATUS, message=str(e))

    def run_pipeline(self) -> Tuple[list[ProcessingResult], Counter]:
        """Executes the full processing pipeline.

        1. Loads and filters metadata.
        2. Uses a ThreadPoolExecutor for parallel I/O-bound processing.
        3. Tracks progress with `rich.progress`.

        Returns:
            A tuple containing a list of all processing results and a Counter
            summarizing the status of processed RSO classes.
        """
        logger.info("Starting image processing pipeline...")
        metadata_records = list(self._load_and_filter_metadata())

        if not metadata_records:
            logger.warning("No metadata records found matching the criteria. Exiting.")
            return [], Counter()

        results: list[ProcessingResult] = []
        class_summary = Counter()

        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Processing images...", total=len(metadata_records)
            )
            # * Use ThreadPoolExecutor for I/O-bound tasks like file operations.
            # * This avoids the GIL limitation present with multiprocessing.
            with ThreadPoolExecutor(max_workers=self.cfg.processing.max_workers) as executor:
                future_to_metadata = {
                    executor.submit(self._simulate_image_processing, record): record
                    for record in metadata_records
                }

                for future in as_completed(future_to_metadata):
                    result = future.result()
                    results.append(result)
                    if result.status == SUCCESS_STATUS:
                        class_summary[result.metadata.rso_class] += 1
                    progress.update(task, advance=1)

        logger.info("Image processing pipeline finished.")
        return results, class_summary
```

#### Main Entry Point
```python
# ================================== Imports ================================== #
# Standard Library
from collections import Counter
from pathlib import Path

# Third-party
import hydra
from loguru import logger
from omegaconf import DictConfig, OmegaConf
from rich.console import Console
from rich.table import Table

# Local Application
from image_processor.processing import ImageProcessor, ProcessingResult
from image_processor.utils import setup_logger

# ================================== Functions ================================ #
def generate_summary_table(
    results: list[ProcessingResult], class_summary: Counter
) -> Table:
    """Creates a rich Table to display the processing summary.

    Args:
        results: A list of all processing results from the pipeline.
        class_summary: A Counter of successfully processed RSO classes.

    Returns:
        A rich Table object ready for printing to the console.
    """
    table = Table(
        title="[bold blue]Image Processing Pipeline Summary[/bold blue]",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Metric", style="dim", width=30)
    table.add_column("Value", justify="right")

    success_count = sum(1 for r in results if r.status == "SUCCESS")
    failure_count = len(results) - success_count

    table.add_row("Total Images Considered", str(len(results)))
    table.add_row("[green]Successful Operations[/green]", str(success_count))
    table.add_row("[red]Failed Operations[/red]", str(failure_count))
    table.add_section()

    if class_summary:
        table.add_row("[bold]Success Count by RSO Class[/bold]", "")
        for rso_class, count in sorted(class_summary.items()):
            table.add_row(f"  - {rso_class}", str(count))

    return table

@hydra.main(config_path="../../conf", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    """Main function orchestrated by Hydra.

    Args:
        cfg: The configuration object populated by Hydra.
    """
    # -------------------------- Initialization -------------------------- #
    console = Console()
    setup_logger(Path(cfg.log_file))
    logger.info(f"Starting [bold cyan]{cfg.app_name}[/bold cyan]...")
    logger.debug(
        f"Full configuration:\n{OmegaConf.to_yaml(cfg)}"
    )

    # -------------------------- Core Logic ------------------------------ #
    try:
        processor = ImageProcessor(cfg)
        results, class_summary = processor.run_pipeline()
    except Exception:
        logger.opt(exception=True).critical("Pipeline execution failed.")
        console.print("[bold red]A critical error occurred. Check the logs for details.[/bold red]")
        return # Exit gracefully

    # -------------------------- Reporting ------------------------------- #
    if not results:
        logger.info("No results to report.")
        console.print("[yellow]Pipeline ran but produced no results to summarize.[/yellow]")
        return

    summary_table = generate_summary_table(results, class_summary)
    console.print(summary_table)
    logger.info("Summary report displayed.")

if __name__ == "__main__":
    main()
```

#### Testing
```python
# ================================== Imports ================================== #
# Standard Library
from pathlib import Path
from collections import Counter

# Third-party
import pytest
from omegaconf import OmegaConf

# Local Application
from src.image_processor.processing import (
    ImageProcessor,
    SUCCESS_STATUS,
    FAILURE_STATUS,
)

# ================================== Fixtures ================================= #
@pytest.fixture
def mock_config() -> OmegaConf:
    """Provides a mock OmegaConf object for testing."""
    return OmegaConf.create({
        "paths": {
            "input_csv": "dummy.csv",
            "output_dir": "test_output",
        },
        "processing": {
            "min_confidence": 0.9,
            "required_class": "satellite",
            "max_workers": 2,
            "simulate_io_delay_seconds": 0,
        }
    })

@pytest.fixture
def metadata_csv_file(tmp_path: Path) -> Path:
    """Creates a temporary metadata CSV file for tests."""
    csv_path = tmp_path / "metadata.csv"
    content = [
        "image_id,file_path,confidence_score,rso_class",
        "img_01,data/img_01.png,0.98,satellite",      # Should pass
        "img_02,data/img_02.png,0.85,debris",          # Fail: low confidence
        "img_03,data/img_03.png,0.95,rocket_body",     # Fail: wrong class
        "img_04,data/img_04.png,0.99,satellite",      # Should pass
        "img_05,data/img_05.png,not_a_float,satellite", # Fail: bad data
    ]
    csv_path.write_text("\n".join(content))
    return csv_path

# =================================== Tests =================================== #
def test_image_processor_initialization(mock_config, tmp_path):
    """Tests that the ImageProcessor initializes correctly and creates dirs."""
    # Arrange
    output_path = tmp_path / "test_output"
    mock_config.paths.output_dir = str(output_path)

    # Act
    processor = ImageProcessor(mock_config)

    # Assert
    assert processor.output_dir == output_path
    assert output_path.exists()
    assert output_path.is_dir()

def test_pipeline_filters_and_processes_successfully(
    mock_config, metadata_csv_file, mocker
):
    """
    Tests the end-to-end pipeline execution, verifying filtering and
    summarization logic.
    """
    # Arrange - Arrange - Arrange
    # * Use mocker to patch the I/O simulation to avoid time.sleep()
    # * and to control its return value for predictable testing.
    mocker.patch(
        "src.image_processor.processing.ImageProcessor._simulate_image_processing",
        # Use a lambda to inspect the input and return a dynamic result
        side_effect=lambda metadata: {
            "status": SUCCESS_STATUS, "metadata": metadata
        }
    )

    # Update the config to point to our test CSV
    mock_config.paths.input_csv = str(metadata_csv_file)
    processor = ImageProcessor(mock_config)

    # Act
    results, class_summary = processor.run_pipeline()

    # Assert - Assert - Assert
    # The list of results should reflect all items that were attempted.
    # The filter should yield only two valid records.
    successful_results = [r for r in results if r['status'] == SUCCESS_STATUS]
    assert len(successful_results) == 2

    # Verify the IDs of the records that should have passed the filter.
    successful_ids = {r['metadata'].image_id for r in successful_results}
    assert successful_ids == {"img_01", "img_04"}

    # The class summary should only count successful operations.
    expected_summary = Counter({"satellite": 2})
    assert class_summary == expected_summary

def test_pipeline_handles_file_not_found(mock_config):
    """Tests that a FileNotFoundError is raised for a non-existent CSV."""
    # Arrange
    mock_config.paths.input_csv = "non/existent/path.csv"
    processor = ImageProcessor(mock_config)

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        processor.run_pipeline()
```
