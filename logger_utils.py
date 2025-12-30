"""
Logger Utility

A versatile logging tool that writes logs to both terminal and file,
with customizable configurations.

# Import the logger (ensure logger_utils.py is in your project directory)
from logger_utils import get_logger

"""



import sys
import os
import time
from datetime import datetime
from contextlib import contextmanager

class TerminalLogger:
    """
    Universal Terminal Logging Utility:
    1. Logs to both terminal and file simultaneously
    2. Supports custom log path, level, and format
    3. Automatically creates log files with timestamps
    4. Compatible with context manager (with statement)
    """
    # Log levels (higher numbers mean more critical logs)
    LOG_LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50
    }

    def __init__(
        self,
        log_dir: str = "logs",
        log_filename: str = None,
        log_level: str = "INFO",
        log_format: str = None,
        overwrite: bool = False
    ):
        """
        Initialize logger instance
        
        :param log_dir: Directory for log files (default: "logs" in current directory)
        :param log_filename: Prefix for log filename (default: generates taskname_timestamp.log)
        :param log_level: Log severity level (DEBUG/INFO/WARNING/ERROR/CRITICAL)
        :param log_format: Custom log format string (default includes timestamp, level, message)
        :param overwrite: Whether to overwrite existing log file (default: append mode)
        """
        # Initialize base parameters
        self.log_dir = os.path.abspath(log_dir)
        self.log_level = self.LOG_LEVELS.get(log_level.upper(), self.LOG_LEVELS["INFO"])
        self.overwrite = overwrite

        # Create log directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)

        # Generate log filename
        if not log_filename:
            task_name = os.path.basename(sys.argv[0]).replace(".py", "") if sys.argv[0] else "task"
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.log_filename = f"{task_name}_{timestamp}.log"
        else:
            self.log_filename = log_filename if log_filename.endswith(".log") else f"{log_filename}.log"
        
        self.log_filepath = os.path.join(self.log_dir, self.log_filename)

        # Configure log format
        if not log_format:
            self.log_format = "[%(asctime)s] [%(level)s] %(message)s"
        else:
            self.log_format = log_format

        # Save original stdout/stderr for restoration
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        # Log file handle
        self.log_file = None

    def _format_log(self, level: str, message: str) -> str:
        """Format log message with specified structure"""
        asctime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.log_format % {
            "asctime": asctime,
            "level": level.ljust(8),  # Align level names (8 characters width)
            "message": message.strip()
        }

    def _write_log(self, level: str, message: str):
        """Write log to both terminal and file (if level meets threshold)"""
        # Filter logs below specified severity level
        if self.LOG_LEVELS.get(level.upper(), 0) < self.log_level:
            return
        
        # Format log message
        formatted_log = self._format_log(level, message)
        
        # Print to terminal
        print(formatted_log, file=self.original_stdout)
        
        # Write to log file
        if self.log_file:
            self.log_file.write(f"{formatted_log}\n")
            self.log_file.flush()  # Force write to disk immediately

    # Log level methods
    def debug(self, message: str):
        """Log a debug message"""
        self._write_log("DEBUG", message)

    def info(self, message: str):
        """Log an info message"""
        self._write_log("INFO", message)

    def warning(self, message: str):
        """Log a warning message"""
        self._write_log("WARNING", message)

    def error(self, message: str):
        """Log an error message"""
        self._write_log("ERROR", message)

    def critical(self, message: str):
        """Log a critical message"""
        self._write_log("CRITICAL", message)

    def capture_terminal_output(self):
        """Redirect stdout/stderr to capture all print statements and errors"""
        # Custom stream wrapper
        class LoggedStream:
            def __init__(self, logger, original_stream, stream_type: str):
                self.logger = logger
                self.original_stream = original_stream
                self.stream_type = stream_type  # stdout/stderr

            def write(self, message):
                if message.strip():  # Ignore empty lines
                    if self.stream_type == "stderr":
                        self.logger.error(message)
                    else:
                        self.logger.info(message)
                self.original_stream.write(message)
                self.original_stream.flush()

            def flush(self):
                self.original_stream.flush()

        # Redirect standard streams
        sys.stdout = LoggedStream(self, self.original_stdout, "stdout")
        sys.stderr = LoggedStream(self, self.original_stderr, "stderr")

    def restore_terminal(self):
        """Restore original stdout/stderr"""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    # Context manager implementation
    def __enter__(self):
        """Open log file and start capturing output when entering context"""
        # Open log file (write/append mode)
        mode = "w" if self.overwrite else "a"
        self.log_file = open(self.log_filepath, mode, encoding="utf-8")
        self.capture_terminal_output()  # Start capturing terminal output
        self.info("===== Logging started =====")
        self.info(f"Log file path: {self.log_filepath}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting context"""
        # Restore terminal streams
        self.restore_terminal()
        # Log exceptions if any occurred
        if exc_type:
            self.error(f"Task exception: {exc_type.__name__} - {exc_val}")
        # Finalize log
        self.info("===== Logging finished =====")
        if self.log_file:
            self.log_file.close()
        # Don't suppress exceptions (let them propagate)
        return False

# Convenience function: quickly create a logger
@contextmanager
def get_logger(
    log_dir: str = "logs",
    log_filename: str = None,
    log_level: str = "INFO",
    overwrite: bool = False
):
    """Quickly create a logger instance (context manager)"""
    logger = TerminalLogger(log_dir, log_filename, log_level, overwrite=overwrite)
    try:
        with logger:
            yield logger
    finally:
        pass

# Test code (executes when running this file directly)
if __name__ == "__main__":
    # Test 1: Basic usage
    with get_logger(log_dir="test_logs", log_filename="test_task") as logger:
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        print("This is a regular print statement (will be captured)")
        # Uncomment to test exception logging
        # 1 / 0
    print(f"Logs saved to: test_logs/test_task.log")
