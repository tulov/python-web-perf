#!/usr/bin/env python3
import asyncio
import aiopg
import random
import string

# static seed to generate the same data all the time
rng = random.Random(0)


dsn = 'dbname=test user=test password=test host=127.0.0.1'


async def go():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('DELETE FROM test')
                for i in range(1_000_000):
                    short_random_string = "".join(
                        rng.choice(string.ascii_letters) for _ in range(20))
                    await cur.execute(f"INSERT INTO test VALUES ({i}, '{short_random_string}')")
    print('Success...')


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(go())
finally:
    loop.close()
