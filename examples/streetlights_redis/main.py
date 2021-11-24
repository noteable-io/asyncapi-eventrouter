import asyncio

import aioredis
import async_timeout
from asyncapi import asyncapi_app

CHANNEL = "light/measured"


async def main():
    redis = aioredis.from_url("redis://localhost")
    async with redis.pubsub() as pubsub:
        await pubsub.subscribe(CHANNEL)
        while True:
            try:
                async with async_timeout.timeout(1):
                    message = await pubsub.get_message(ignore_subscribe_messages=True)
                    if message is not None:
                        await asyncapi_app.process(message["data"].decode("utf-8"))
                    await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass


if __name__ == "__main__":
    asyncio.run(main())
