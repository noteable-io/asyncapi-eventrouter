# Streetlights Websockets Example

This example implements the minimal [Streetlights](https://www.asyncapi.com/docs/tutorials/streetlights) data stream from the AsyncAPI documentation, although it uses FastAPI/Websockets as the broker instead of `mqtt`.

## Install

Make sure Poetry's virtual environment is setup and the `asyncapi-eventrouter` is installed alongside dependencies.

1. `poetry use 3.9`
2. `poetry install`
3. `poetry shell`

## Run

1. Start the server: `uvicorn main:app --reload`
2. Send measurement data to the server with `python cli.py send`.  See `python cli.py --help` for more options.


## View schema

The AsyncAPI schema is available in this example via the CLI: `python cli.py schema`.  Optionally use `python cli.py schema --as-json` to format in JSON instead of YAML.

```
asyncapi: 2.2.0
channels:
  light/measured:
    publish:
      LightMeasured:
        payload:
          properties:
            id:
              description: ID of the streetlight.
              gte: 0
              title: Id
              type: integer
            lumens:
              description: Light intensity measured in lumens.
              gte: 0
              title: Lumens
              type: integer
            sentAt:
              description: Date and time when the message was sent.
              format: date-time
              title: Sentat
              type: string
          required:
          - id
          - lumens
          - sentAt
          title: LightMeasured
          type: object
```
