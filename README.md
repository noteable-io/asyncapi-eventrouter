# asyncapi-eventrouter

*Work in Progress*

Write Python code for Event-Driven Architectures!  `asyncapi-eventrouter` is a prototype library for creating Websocket, PubSub, and other asynchronous frameworks with message validation and automatic schema documentation in the [AsyncAPI](https://www.asyncapi.com/) specification.  It's heavily inspired by how [FastAPI](https://fastapi.tiangolo.com/) documents REST endpoints in the [OpenAPI](https://swagger.io/specification/) specification.



# Development

This project uses [poetry](https://python-poetry.org/) and [pre-commit](https://pre-commit.com/) for development.

1. `poetry env use 3.9` will create a `.venv` directory in your `asyncapi-eventrouter` directory
2. `poetry install` will install `asyncapi-eventrouter` and all dependencies into that virtual environment
3. `pre-commit run --all-files` will show you what will be executed any time you `git commit`.

## Skip Pre-commit

If the `pre-commit` hooks can not be easily resolved, you can still commit using `git commit --no-verify`.
