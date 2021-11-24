from asyncapi import asyncapi_app
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            content = await websocket.receive_text()
            response = await asyncapi_app.process(content)
            await websocket.send_json(response)
        except WebSocketDisconnect:
            break


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
