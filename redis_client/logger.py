"""File to define the default logger config."""

import logging
from datetime import datetime
from typing import List

from custom_types import LogLevel


def init_logger(log_level: str = "DEBUG") -> None:
	"""
	Remove all the dependencies debug, info and warning and set the default logging config.
	:param log_level: an int to set which log level has to be defined.
		you can use: [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR].
	"""
	# Define basic config for logs (date format,...)
	# Will search for a LOG_LEVEL venv variable, if there is not, it will set "DEBUG" by default.
	logging.basicConfig(
		level=log_level,
		handlers=[
			# Write logs to file
			logging.FileHandler(f"logs/{datetime.now().strftime('%d-%m-%Y_%H:%M')}.log"),
			# Allow the logger to also log in console
			logging.StreamHandler(),
		],
		format="%(asctime)s %(levelname)-8s %(name)-20s -> %(message)s",
		datefmt="%d/%m/%Y %H:%M:%S",
	)

	return None


def filter_external_logging(loggers_to_filter: List[str], log_level: LogLevel) -> None:
	"""
	Helper function to filter the logs from external libraries.
	That helps to be able to have readable logs.
	:param loggers_to_filter: The list of loggers to filter.
		(usually the name of the lib, can be followed by modules' name)
	:param log_level: The level of logs you want for external libs. (Only show warning, errors, info,...)
	"""
	for logger_name in loggers_to_filter:
		logging.getLogger(logger_name).setLevel(log_level)

	return None
