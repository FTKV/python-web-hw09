import configparser

from mongoengine import connect
import redis
from redis_lru import RedisLRU


config = configparser.ConfigParser()
config.read("first/config.ini")

driver_sync = config.get("DB", "driver_sync")
user = config.get("DB", "user")
password = config.get("DB", "password")
host = config.get("DB", "host")
dbname = config.get("DB", "dbname")

# connect to cluster on AtlasDB with connection string

client_mongo = connect(
    host=f"{driver_sync}://{user}:{password}@{host}/{dbname}", ssl=True
)

try:
    client_redis = redis.Redis(host="localhost", port=6379, db=0)
    client_redis.ping()  # This will attempt to ping the server, and if successful, you're connected.
    cache = RedisLRU(client_redis)
except redis.ConnectionError:
    print("Could not connect to Redis")
