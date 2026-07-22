"""
logger_config.py
Configures logging so agent activity is visible in the console
and saved to a log file for review/debugging.
"""

import logging
import os
from datetime import datetime


def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_filename = f"logs/agent_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logger = logging.getLogger("weather_agent")
    logger.setLevel(logging.INFO)

    # this to avoid duplicate handlers if setup_logger() gets called more than once
    if logger.handlers:
        return logger

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Log to file
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info(f"Logging started. Log file: {log_filename}")
    return logger