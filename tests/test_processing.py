import pytest
from pydantic import BaseModel, ValidationError

from asyncapi_eventrouter import Application


@pytest.mark.asyncio
async def test_simple_message():
    app = Application()

    class Foo(BaseModel):
        value: str

    @app.subscribe(channel_name="test-channel", event_name="test-event")
    async def callback(foo: Foo):
        return repr(foo)

    message = """{"channel": "test-channel", "event": "test-event", "data": {"value": "123"}}"""
    response = await app.process(message)
    assert response == "Foo(value='123')"


@pytest.mark.asyncio
async def test_unhandled_message():
    app = Application()
    message = '{"channel": "test-channel", "event": "test-event", "data": {"value": "123"}}'
    response = await app.process(message)
    assert response is None


@pytest.mark.asyncio
async def test_invalid_message():
    app = Application()
    message = """{"channel": "test-channel", "data": {"value": "123"}}"""
    with pytest.raises(ValidationError) as e:
        response = await app.process(message)
    assert e.value.errors() == [
        {"loc": ("event",), "msg": "field required", "type": "value_error.missing"}
    ]
