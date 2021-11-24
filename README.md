# asyncapi-eventrouter

*Work in Progress*

Write Python code for Event-Driven Architectures!  The **`asyncapi-eventrouter`** prototype library creates Websocket,
PubSub, and other asynchronous frameworks with message validation and automatic schema documentation in the
[AsyncAPI](https://www.asyncapi.com/) specification.  It's heavily inspired by how
[FastAPI](https://fastapi.tiangolo.com/) documents REST endpoints in the [OpenAPI](https://swagger.io/specification/)
specification.

## Example

What would the [Streetlights API](https://www.asyncapi.com/docs/tutorials/streetlights#creating-the-asyncapi-file) look like in Python code with `asyncapi-eventrouter`?

```python
# asyncapi.py
from pydantic import BaseModel, Field
from datetime import datetime
from asyncapi_eventrouter import Application

asyncapi_app = Application()

class LightMeasured(BaseModel):
    id: int = Field(..., gte=0, description="ID of the streetlight.")
    lumens: int = Field(..., gte=0, description="Light intensity measured in lumens.")
    sentAt: datetime = Field(..., description="Date and time when the message was sent.")

@asyncapi_app.subscribe(channel_name="light/measured",
                        event_name="LightMeasured")
async def record_measurement(measurement: LightMeasured):
    # record to db or take some other action
    return {'received': datetime.now()}
```

```python
# main.py
from fastapi import FastAPI, WebSocket
from asyncapi import asyncapi_app

app = FastAPI()

@app.websocket('/ws')
async def ws(websocket: Websocket):
    await ws.accept()
    while True:
        content = await websocket.receive_text()
        response = await asyncapi_app.process(content)
        await websocket.send_json(response)

@app.get('/ws-schema')
async def ws_schema():
    return asyncapi_app.schema()
```

```python
# client.py
import asyncio
import json
from datetime import datetime

import websockets

async def send_measurement():
    data = {"id": 123, "lumens": 42, "sentAt": datetime.now().isoformat()}
    event = {"channel": "light/measured", "event": "LightMeasured", "data": data}
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        await ws.send(json.dumps(event))

if __name__ == '__main__':
    asyncio.run(send_measurement())
```

Last but not least, you can view the spec by visiting that `/ws-schema` endpoint or by importing the `asyncapi_app` and dumping the schema.

```python
from asyncapi import asyncapi_app
import yaml

print(yaml.dump(asyncapi_app.schema())
>>> asyncapi: 2.2.0
    channels:
    light/measured:
        publish:
        LightMeasured:
            payload:
            properties:
                id:
                description: ID of the streetlight.
                gte: 0
                title: Id
                type: integer
                lumens:
                description: Light intensity measured in lumens.
                gte: 0
                title: Lumens
                type: integer
                sentAt:
                description: Date and time when the message was sent.
                format: date-time
                title: Sentat
                type: string
            required:
            - id
            - lumens
            - sentAt
            title: LightMeasured
            type: object
```


## Development

This project uses [poetry](https://python-poetry.org/) and [pre-commit](https://pre-commit.com/) for development.

1. `poetry env use 3.9` will create a `.venv` directory in your `asyncapi-eventrouter` directory.
2. `poetry install` will install `asyncapi-eventrouter` and all dependencies into that virtual environment.
3. `pre-commit run --all-files` will show you what will be executed any time you `git commit`.

### Skip Pre-commit

If the `pre-commit` hooks can not be easily resolved, you can still commit using `git commit --no-verify`.


## Inspiration and gratitude

The useful FastAPI project inspires this project. Any code snippets from FastAPI are given credit and attribution in the
source code. We are thankful to the FastAPI community for their work.
