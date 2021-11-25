"""AsyncAPI compatible Application"""
import collections
import inspect
import warnings
from typing import Callable, Coroutine

from pydantic import BaseModel


class Subscription:
    def __init__(self, func: Callable[..., Coroutine]):
        self.func = func
        self.signature = inspect.signature(func)
        func_params = list(self.signature.parameters.values())
        if len(func_params) != 1:
            raise Exception()
        self.model = func_params[0].annotation

    async def process(self, data: dict):
        validated = self.model(**data)
        return await self.func(validated)

    def schema(self):
        return {"payload": self.model.schema()}


class Publish:
    def __init__(self, model: BaseModel):
        self.model = model

    def schema(self):
        return {"payload": self.model.schema()}


class Channel:
    def __init__(self):
        self.publishers = {}
        self.subscribers = {}

    def register_subscription(self, event_name: str, func: Callable[..., Coroutine]):
        if event_name in self.subscribers:
            warnings.warn(f"overwriting existing subscription for {event_name}")
        sub = Subscription(func=func)
        self.subscribers[event_name] = sub

    def register_publish(self, event_name: str, model: BaseModel):
        if event_name in self.publishers:
            warnings.warn(f"overwriting existing publish for {event_name}")
        pub = Publish(model=model)
        self.publishers[event_name] = pub

    def subscribe(self, event_name: str):
        def decorator(func):
            self.register_subscription(event_name, func)
            return func

        return decorator

    async def process(self, event_name: str, data: dict):
        if event_name in self.subscribers:
            return await self.subscribers[event_name].process(data)

    def schema(self):
        out = collections.defaultdict(dict)
        for event_name, subscription in self.subscribers.items():
            out["publish"][event_name] = subscription.schema()
        for event_name, publisher in self.publishers.items():
            out["subscribe"][event_name] = publisher.schema()
        return dict(out)


class ChannelRouter:
    def __init__(self):
        self.channels = {}

    def register_subscription(
        self, channel_name: str, event_name: str, func: Callable[..., Coroutine]
    ):
        if channel_name not in self.channels:
            self.channels[channel_name] = Channel()
        return self.channels[channel_name].register_subscription(event_name, func)

    def subscribe(self, channel_name: str, event_name: str):
        def decorator(func):
            self.register_subscription(channel_name, event_name, func)
            return func

        return decorator

    async def process(self, channel_name: str, event_name: str, data: dict):
        if channel_name in self.channels:
            return await self.channels[channel_name].process(event_name, data)

    def schema(self):
        out = {}
        for name, channel in self.channels.items():
            out[name] = channel.schema()
        return out
