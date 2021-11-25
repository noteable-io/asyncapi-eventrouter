import asyncio

import mqttools
from asyncapi import asyncapi_app

CHANNEL = "light/measured"


async def main():
    client = mqttools.Client("localhost", 1883)
    await client.start()
    await client.subscribe(CHANNEL)

    while True:
        topic, message = await client.messages.get()
        if topic is None:
            print("Broker connection lost!")
            break
        await asyncapi_app.process(message.decode("utf-8"))


if __name__ == "__main__":
    asyncio.run(main())
