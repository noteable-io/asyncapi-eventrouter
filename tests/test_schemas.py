import pytest
from pydantic import BaseModel

from asyncapi_eventrouter import Application


@pytest.mark.asyncio
async def test_bare_app():
    app = Application()
    assert app.schema() == {"asyncapi": "2.2.0", "channels": {}}


@pytest.mark.asyncio
async def test_app_with_subscribe_decorator():
    app = Application()

    class Foo(BaseModel):
        value: str

    @app.subscribe(channel_name="test-channel", event_name="test-event")
    async def callback(foo: Foo):
        pass

    assert app.schema() == {
        "asyncapi": "2.2.0",
        "channels": {
            "test-channel": {
                "publish": {
                    "test-event": {
                        "payload": {
                            "title": "Foo",
                            "type": "object",
                            "properties": {"value": {"title": "Value", "type": "string"}},
                            "required": ["value"],
                        }
                    }
                }
            }
        },
    }
