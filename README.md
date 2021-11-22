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
from pydantic import BaseModel, Field
from datetime import datetime
from asyncapi_eventrouter import AsyncRouter

router = AsyncRouter()

class LightMeasured(BaseModel):
    id: int = Field(..., gte=0, description="ID of the streetlight.")
    lumens: int = Field(..., gte=0, description="Light intensity measured in lumens.")
    sentAt: datetime = Field(..., description="Date and time when the message was sent.")

@router.subscribe(channels="light/measured", name="LightMeasured")
async def record_measurement(measurement: LightMeasured):
    # record to db or take some action
    return
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
