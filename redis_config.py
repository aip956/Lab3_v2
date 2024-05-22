import aioredis
from fastapi import Depends

REDIS_URL = "redis://localhost:6379"

async def create_redis_pool():
    return await aioredis.create_redis_pool(
        REDIS_URL,
        encoding="utf-8",
        minsize=5,
        maxsize=10
    )


# class RedisClient:
#     def __init__(self):
#         self.pool = None

#     async def __aenter__(self):  # Enter method for context management
#         self.pool = await aioredis.create_redis_pool(REDIS_URL, encoding="utf-8", minsize=5, maxsize=10)
#         return self.pool

#     async def __aexit__(self, exc_type, exc, tb):  # Exit method for handling closure
#         self.pool.close()
#         await self.pool.wait_closed()


async def get_redis_client():
    pool = await create_redis_pool()
    # redis = await aioredis.create_redis_pool(REDIS_URL, encoding="utf=8", minsize=5, maxsize=10)
    # pool = redis.ConnectionPool(host='redis', port=6379, db=0, decode_responses=True, max_connections=10)
    # return redis.Redis(connection_pool=pool)
    try:
        yield pool
    finally:
        pool.close() # Make sure connections are closed
        await pool.wait_closed()
    # return RedisClient()


# Dependency to be used with FastAPI endpoints
async def redis_dependency():
    # async with get_redis_client() as client:
    #     yield client
    return Depends(get_redis_client)
    # client = get_redis_client()
    
