"""
Logger Configuration Module
===========================

Configures logging for Python applications.

Example usage:
--------------
    from logger import configure_logging, get_logger

    configure_logging()
    logger = get_logger(__name__)
    logger.info("Logging is configured.")

Author:
-------
- Rodrigo de Souza Rampazzo <rosorzz@protonmail.com>
- GitHub: https://github.com/rzz0

License:
--------
MIT License
"""

import logging
import logging.handlers
import os
from typing import Optional


def configure_logging(
    log_filename: str = "LOG_app.log",
    log_level: int = logging.INFO,
    log_dir: Optional[str] = None,
    max_bytes: int = 10**6,
    backup_count: int = 3,
) -> None:
    """
    Configures logging for the application.

    Args:
        log_filename (str): Name of the log file. Default is 'LOG_app.log'.
        log_level (int): Log level. Default is logging.INFO.
        log_dir (Optional[str]): Directory where the log file will be saved.
        Default is None, which means the current directory.
        max_bytes (int): Maximum size of the log file in bytes before
        rolling over. Default is 10^6 bytes.
        backup_count (int): Number of backup log files to keep. Default is 3.
    """
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir or "", log_filename)

    # Configure the FileHandler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file_path, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
    )

    # Configure the StreamHandler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
    )

    # Configure the root logger
    logging.basicConfig(level=log_level, handlers=[file_handler, console_handler])


def get_logger(name: str) -> logging.Logger:
    """
    Gets a logger with the specified name.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
