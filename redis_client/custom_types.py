"""File that contains custom types for the python logging module."""
from typing import Literal

LogLevel = Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]