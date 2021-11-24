from datetime import datetime

from pydantic import BaseModel, Field

from asyncapi_eventrouter import Application

asyncapi_app = Application()


class LightMeasured(BaseModel):
    id: int = Field(..., gte=0, description="ID of the streetlight.")
    lumens: int = Field(..., gte=0, description="Light intensity measured in lumens.")
    sentAt: datetime = Field(..., description="Date and time when the message was sent.")


@asyncapi_app.subscribe(channel_name="light/measured", event_name="LightMeasured")
async def record_measurement(measurement: LightMeasured):
    # record to db or take some other action
    print(repr(measurement))
    return {"received": datetime.now().isoformat()}
