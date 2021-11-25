# FastAPI Websockets Example

This example follows the well-written [FastAPI Websockets](https://fastapi.tiangolo.com/advanced/websockets/) documentation, showing how to add in `asyncapi-eventrouter` to a minimal websocket application.

## Install

Make sure Poetry's virtual environment is setup and the `asyncapi-eventrouter` is installed alongside the optional "examples" dependencies.

1. `poetry use 3.9`
2. `poetry install -E examples`
3. `poetry shell`

## Run

From the Poetry virtual environment shell: `uvicorn main:app --reload`

## View schema

The basic Websocket request/reply behavior should look nearly identical to the vanilla FastAPI websocket example.  However you can view the JSON AsyncAPI schema for the websocket-app at `http://localhost:8000/ws-schema`.  It should render as --

```
{
    "asyncapi": "2.2.0",
    "channels": {
        "demo": {
            "publish": {
                "msg": {
                    "payload": {
                        "title": "Text",
                        "type": "object",
                        "properties": {
                            "text": {
                                "title": "Text",
                                "type": "string"
                            }
                        },
                        "required": [
                            "text"
                        ]
                    }
                }
            }
        }
    }
}
```
