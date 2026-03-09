import asyncio
import asyncpg

async def test():
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="jobcatcher",
        password="jobcatcherpass",
        database="jobcatcher"
    )

    print("Connected to database!")

    await conn.close()

asyncio.run(test())