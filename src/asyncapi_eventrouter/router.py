from typing import Any, Coroutine, Dict, List, Optional, Union

from pydantic import BaseModel

from asyncapi_eventrouter.asyncapi.utils import get_asyncapi


class ChannelAction:
    def __init__(
        self,
        channel: str,
        name: str,
        publish_type: Optional[BaseModel],
        subscribe_type: Optional[BaseModel],
        subscribe_callback: Optional[Coroutine],
    ):
        self.channel = channel
        self.name = name
        self.publish_type = publish_type
        self.subscribe_type = subscribe_type
        self.subscribe_callback = subscribe_callback


class AsyncRouter:
    def __init__(
        self,
        *,
        routes: Optional[List[ChannelAction]] = None,
        title: str = "AsyncRouter",
        description: str = "",
        version: str = "0.1.0",
        asyncapi_tags: Optional[List[Dict[str, Any]]] = None,
        servers: Optional[List[Dict[str, Any]]] = None,
        terms_of_service: Optional[str] = None,
        contact: Optional[Dict[str, Union[str, Any]]] = None,
        license_info: Optional[Dict[str, Union[str, Any]]] = None,
    ):
        self.routes = routes or []
        self.title = title
        self.description = description
        self.version = version
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license_info = license_info
        self.servers = servers or []
        self.asyncapi_tags = asyncapi_tags

        # Placeholder to cache schema when self.asyncapi() is called
        self.asyncapi_schema: Optional[Dict[str, Any]] = None
        self.asyncapi_version = "2.2.0"

        # TODO: add default_content_type (as default_response_class ?)

    def asyncapi(self):
        "Return the AsyncAPI schema for this router as a dictionary"
        # Only gets built one time, then saved statically
        if not self.asyncapi_schema:
            self.asyncapi_schema = get_asyncapi(
                title=self.title,
                version=self.version,
                asyncapi_version=self.asyncapi_version,
                description=self.description,
                terms_of_service=self.terms_of_service,
                contact=self.contact,
                license_info=self.license_info,
                routes=self.routes,
                tags=self.asyncapi_tags,
                servers=self.servers,
            )
        return self.asyncapi_schema
