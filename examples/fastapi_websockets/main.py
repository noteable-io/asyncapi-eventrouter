import json

from fastapi import FastAPI, Response, WebSocket
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import asyncapi_eventrouter  # type: ignore

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var wsEvent = {"channel": "demo",
                               "event": "msg",
                               "data": {"text": input.value},
                               }
                ws.send(JSON.stringify(wsEvent))
                input.value = ''
                event.preventDefault()
            };
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


asyncapi_app = asyncapi_eventrouter.Application()


class Text(BaseModel):
    text: str


@asyncapi_app.subscribe(channel_name="demo", event_name="msg")
def echo(data: Text):
    return repr(data)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        content = await websocket.receive_text()
        response = asyncapi_app.process(content)
        await websocket.send_text(response)


class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content):
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")


@app.get("/ws-schema", response_class=PrettyJSONResponse)
def ws_schema():
    return asyncapi_app.schema()


if __name__ == "__main__":
    import uvicorn  # type: ignore

    uvicorn.run(app, debug=True)
