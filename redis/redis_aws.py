import redis
from dataclasses import dataclass
import os


@dataclass
class RedisSettings:
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", None)


def connect_redis(settings: RedisSettings) -> redis.Redis:
    """ Connects to Redis using the provided settings. """
    try:
        client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            ssl=True,
            decode_responses=True  # Decodes responses as strings; no need for .decode('utf-8')
        )
        client.ping()  # Check the connection
        print("Successfully connected to Redis.")
        return client
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        raise


if __name__ == '__main__':
    try:
        settings = RedisSettings()
        redis_client = connect_redis(settings)
    except Exception as e:
        print(f"Error initializing Redis client: {e}")

# Redis commands
# redis_client.set("key", "value", ex=60)  # Set key, value, and TTL of 60 seconds
# value = redis_client.get("key")          # Get the value of the key
# value = redis_client.ttl("key")          # Get the TTL of the key

# redis_client.set("key", "value", ex=60)  # Update the key with a new value and TTL

# redis_client.delete("key")               # Delete the key

# redis_client.flushdb()                   # Clear the current database
# keys = redis_client.keys('*')           # Get all keys from the database
# for key in keys:
#     print(key)                           # Print each key
