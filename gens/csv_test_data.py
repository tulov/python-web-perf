#!/usr/bin/env python3
import asyncio
from aiopg.sa import create_engine
import random
import string

# static seed to generate the same data all the time
rng = random.Random(0)


async def go():
    async with create_engine(user='postgres',
                             database='test',
                             host='127.0.0.1',
                             password='postgres') as engine:
        async with engine.acquire() as conn:
            await conn.execute('DELETE FROM test')
            for i in range(1_000_000):
                short_random_string = "".join(
                    rng.choice(string.ascii_letters) for _ in range(20))
                await conn.execute(f"INSERT INTO test VALUES ({i}, '{short_random_string}')")


asyncio.run(go())
