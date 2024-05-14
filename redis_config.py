import redis

class RedisClient:
    _instance = None

    @staticmethod
    def get_instance():
        if RedisClient._instance is None:
            # Create connection pool
            pool = redis.ConnectionPool(host='redis', port=6379, db=0, decode_responses=True, max_connections=10)
            RedisClient._instance = redis.Redis(connection_pool=pool)
        return RedisClient._instance
    
def get_redis_client():
    return RedisClient.get_instance()