from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, List, Optional

import asyncapi_eventrouter
from asyncapi_eventrouter.asyncapi.models import AsyncAPI
from asyncapi_eventrouter.encoders import jsonable_encoder

# reference ChannelAction through base library to avoid circular imports
# since router.py imports get_asyncapi function


def get_asyncapi(
    *,
    asyncapi_version: str = "2.2.0",
    title: str,
    version: str,
    description: Optional[str] = None,
    servers: Optional[List[Dict[str, Any]]] = None,
    terms_of_service: Optional[str] = None,
    contact: Optional[Dict[str, Any]] = None,
    license_info: Optional[Dict[str, Any]] = None,
    routes: List[asyncapi_eventrouter.router.ChannelAction],  # type: ignore
    tags: Optional[List[Dict[str, Any]]] = None,
):
    info: Dict[str, Any] = {"title": title, "version": version}
    if description:
        info["description"] = description
    if terms_of_service:
        info["termsOfService"] = terms_of_service
    if contact:
        info["contact"] = contact
    if license_info:
        info["license"] = license_info
    output: Dict[str, Any] = {"asyncapi": asyncapi_version, "info": info}
    if servers:
        output["servers"] = servers
    if tags:
        output["tags"] = tags

    channels: Dict[str, Dict[str, Any]] = defaultdict(dict)
    for route in routes:
        pass
    output["channels"] = channels

    schema = AsyncAPI(**output)
    return jsonable_encoder(schema, by_alias=True, exclude_none=True)
