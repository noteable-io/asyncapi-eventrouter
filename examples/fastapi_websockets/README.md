
# Install

1. Enter into the Poetry virtual environment
    - `poetry use 3.9`
    - `poetry install`
    - `poetry shell`

2. Install the requirements for this sample app
    - `pip install -r requirements.txt`

# Run

From the Poetry virtual environment shell:
    - `uvicorn main:app --reload`

# View schema

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
