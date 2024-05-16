import redis

# class RedisClient:
#     _instance = None
# # am i creating connec pool each req
# #benchmarking for time to each command
# # hook up like getdb
#     @staticmethod
#     def get_instance():
#         if RedisClient._instance is None:
#             # Create connection pool
#             RedisClient._instance = redis.Redis(connection_pool=pool)
#         return RedisClient._instance
    
def get_redis_client():
    pool = redis.ConnectionPool(host='redis', port=6379, db=0, decode_responses=True, max_connections=10)
    return redis.Redis(connection_pool=pool)

def redis_dependency():
    client = get_redis_client()
    try:
        yield client
    finally:
        client.close() # Make sure connections are closed