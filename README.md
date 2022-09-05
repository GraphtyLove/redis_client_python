# Redis client

Simple Redis client for python.

It has been made to simplify working with Redis in python.

## Usage
Instantiate `Cache()`, give the Redis `host`, `port` and `db`.

Then you can get a cached entry with `Cache.get_data_from_cache()` and add an entry to Redis with `Cache.save_data_to_cache()`

**⚠️The data send to cache NEEDS TO BE A DICTIONARY! ⚠️**

### Code example

```python
from redis_client.client import Cache
from time import sleep
from tpying import Dict

# Redis Configuration
cache = Cache(redis_host="localhost", redis_port=6379, redis_db=0, log_level="INFO")

def username_expander(username: str) -> Dict[str, str]:
    """Example of a function that require caching."""
    
    # Key that will be use to retrieve cached data
    # Note that I include the parameter 'username' in the key to make sure we only cache unique value.
    key = f"username_expander:{username}"
    
    # Check if the data is already caches
    cached_data = cache.get_data_from_cache(key)
    
    # Return it if yes
    if cached_data:
        return cached_data
    
    data = {"expanded_username": f"{username}_123"}
    
    # Save data to cache with an expiration time of 12 hours
    cache.save_data_to_cache(key, data, expiration_in_hours=12)
    
    return data
```