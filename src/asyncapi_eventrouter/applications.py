from typing import Any, Callable, Coroutine

from pydantic import BaseModel

from .routers import ChannelRouter


class Event(BaseModel):
    channel: str
    event: str
    data: Any


class Application:
    def __init__(self):
        self.router = ChannelRouter()

    def register_subscription(
        self, channel_name: str, event_name: str, func: Callable[..., Coroutine]
    ):
        return self.router.register_subscription(channel_name, event_name, func)

    def subscribe(self, channel_name: str, event_name: str):
        def decorator(func):
            self.register_subscription(channel_name, event_name, func)
            return func

        return decorator

    async def process(self, message: str):
        event = Event.parse_raw(message)
        return await self.router.process(
            channel_name=event.channel, event_name=event.event, data=event.data
        )

    def schema(self):
        out = {"asyncapi": "2.2.0"}
        out["channels"] = self.router.schema()
        return out
