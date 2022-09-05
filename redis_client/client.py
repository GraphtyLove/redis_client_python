"""File that contains the Redis Client."""
import sys
from typing import Dict, Any

import redis
import json
from datetime import timedelta
from logging import getLogger

from redis_client.custom_types import LogLevel
from redis_client.logger import init_logger


class Cache:
	def __init__(
		self,
		redis_host: str = "localhost",
		redis_port: int = 6379,
		redis_db: int = 0,
		log_level: LogLevel = "INFO",
	):
		# Configure logging
		init_logger(log_level)
		self._logger = getLogger("redis_client.client.Cache")
		self._logger.setLevel(log_level)

		# Establish connection with Redis.
		try:
			client = redis.Redis(
				host=redis_host,
				port=redis_port,
				db=redis_db,
			)
			# Verify that Redis is responding
			ping = client.ping()
			if ping is True:
				self.client = client
			else:
				self._logger.error("Connection established but Redis not responding to ping!")
		# Log error and stop the process if not responding
		except redis.ConnectionError as ex:
			self._logger.critical(f"Redis Connection Error: {ex}. Shutting down.")
			sys.exit(1)

	def get_data_from_cache(self, key: str) -> Dict[Any] | None:
		"""
		Get data from redis.

		:param key: the key used to store the data in Redis.
		:return data: A dictionary with the data cached if found, None if nothing found with the key.
		"""

		data = self.client.get(key)
		if data is None:
			self._logger.debug(f"Data with key: {key} not found in cache.")
			return None
		data = data.decode("UTF-8")
		data_dict = json.loads(data)
		self._logger.debug(f"Data with key {key} found from cache")
		return data_dict

	def save_data_to_cache(self, key: str, value: Dict[Any], expiration_in_hours: int = 24) -> bool:
		"""
		Save data to redis.

		:param key: the key used to store the data in Redis.
		:param value: the value associated to the key to save in Redis. THIS NEEDS TO BE A DICTIONARY!
		:param expiration_in_hours: The number of hours before expiration of the cached data in Redis. Default is 24h.
		:return state: True if the data is well saved in Redis, False if not.
		"""
		str_value = json.dumps(value)
		state = self.client.setex(
			key,
			timedelta(hours=expiration_in_hours),
			value=str_value,
		)
		self._logger.debug(f"Data with key: {key} saved to Redis!")
		return state
