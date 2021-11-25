import asyncio
import json
from datetime import datetime

import mqttools
import typer
import yaml
from asyncapi import asyncapi_app

app = typer.Typer()

CHANNEL = "light/measured"


async def send_measurement(id: int = 123, lumens: int = 42):
    data = {"id": id, "lumens": lumens, "sentAt": datetime.now().isoformat()}
    event = {"channel": CHANNEL, "event": "LightMeasured", "data": data}
    async with mqttools.Client("localhost", 1883) as client:
        client.publish(CHANNEL, json.dumps(event).encode("utf-8"))


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
