# terminal-logger
A lightweight Python logging tool that simultaneously writes logs to both terminal and file, with flexible configuration options.

## Features

- Outputs: logs to both terminal and file
- Automatic log directory creation
- Customizable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Timestamp integration for log filenames
- Context manager support (auto-cleanup with `with` statement)
- Captures standard output (print statements) and errors
- Easy to integrate with existing projects

## Installation

1. Download `logger_utils.py`
2. Place it in your project directory
3. Import using `from logger_utils import get_logger`

## Basic Usage

```python
from logger_utils import get_logger

# Basic logging example
with get_logger() as logger:
    logger.debug("Debug message - detailed information for debugging")
    logger.info("Info message - confirmation that things are working")
    logger.warning("Warning message - something unexpected happened")
    logger.error("Error message - failed to perform an operation")
    logger.critical("Critical message - serious error, program may exit")


### Advanced Configuration

## Custom Log Directory and Filename

```python
with get_logger(
    log_dir="application_logs",  # Custom log directory
    log_filename="backend_service",  # Log file prefix
    log_level="DEBUG"  # Show all log levels down to DEBUG
) as logger:
    logger.info("Starting backend service...")
    # Your code here
```

## Overwrite Existing Logs

```python
# Overwrite mode (instead of appending)
with get_logger(
    log_dir="temp_logs",
    log_filename="session",
    overwrite=True  # Will overwrite existing file
) as logger:
    logger.info("This will replace existing session.log")
```

## Integrate with Existing Code

```python
def main_task():
    with get_logger(
        log_dir="task_logs",
        log_filename="data_processor",
        log_level="INFO"
    ) as logger:
        try:
            logger.info("Starting data processing...")
            # Your main logic here
            logger.info("Data processing completed successfully")
        except Exception as e:
            logger.critical(f"Task failed: {str(e)}")
            raise  # Re-raise to ensure proper error handling

if __name__ == "__main__":
    main_task()
```


### Log Levels
|Level	|Description|
|---|---|
|DEBUG	|Detailed information, useful for debugging|
|INFO	|Confirmation that things are working as expected|
|WARNING	|An indication that something unexpected happened (default level)|
|ERROR	|Due to a more serious problem, the software has not been able to perform some function|
|CRITICAL	|A serious error, indicating that the program itself may be unable to continue running|










