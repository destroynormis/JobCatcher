import asyncpg

async def create_pool():
    pool = await asyncpg.create_pool(
        host="localhost",
        port=5432,
        user="jobcatcher",
        password="jobcatcherpass",
        database="jobcatcher"
    )
    return pool