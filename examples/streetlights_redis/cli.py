import asyncio
import json
from datetime import datetime

import aioredis
import typer
import yaml
from asyncapi import asyncapi_app

app = typer.Typer()

CHANNEL = "light/measured"


async def send_measurement(id: int = 123, lumens: int = 42):
    data = {"id": id, "lumens": lumens, "sentAt": datetime.now().isoformat()}
    event = {"channel": CHANNEL, "event": "LightMeasured", "data": data}
    redis = aioredis.from_url("redis://localhost")
    await redis.publish(CHANNEL, json.dumps(event))


@app.command()
def send(id: int = 123, lumens: int = 42):
    asyncio.run(send_measurement(id, lumens))


@app.command()
def schema(as_json: bool = False):
    schema = asyncapi_app.schema()
    if as_json:
        print(json.dumps(schema, indent=2))
    else:
        print(yaml.dump(schema))


if __name__ == "__main__":
    app()
