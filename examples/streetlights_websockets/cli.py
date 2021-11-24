import asyncio
import json
from datetime import datetime

import typer
import websockets
import yaml
from asyncapi import asyncapi_app

app = typer.Typer()


async def send_measurement(id: int = 123, lumens: int = 42):
    data = {"id": id, "lumens": lumens, "sentAt": datetime.now().isoformat()}
    event = {"channel": "light/measured", "event": "LightMeasured", "data": data}
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        await ws.send(json.dumps(event))
        print(await ws.recv())


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
