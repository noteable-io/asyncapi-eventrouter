"""
Model the AsyncAPI specification v2.2.0

https://www.asyncapi.com/docs/specifications/v2.2.0
"""
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyUrl, BaseModel, Field

VALID_PROTOCOLS = [
    "amqp",
    "amqps",
    "http",
    "https",
    "ibmmq",
    "jms",
    "kafka",
    "kafka-secure",
    "anypointmq",
    "mqtt",
    "secure-mqtt",
    "stomp",
    "stomps",
    "ws",
    "wss",
    "mercure",
]

# TODO: Order these in some intuitive way?
# To consider: Some base model that handles Config.extra = "allow"


class ServerBinding(BaseModel):
    class Config:
        extra = "allow"


class ChannelBinding(BaseModel):
    class Config:
        extra = "allow"


class OperationBinding(BaseModel):
    class Config:
        extra = "allow"


class MessageBinding(BaseModel):
    class Config:
        extra = "allow"


class ExternalDoc(BaseModel):
    description: Optional[str]
    url: AnyUrl

    class Config:
        extra = "allow"


class Tag(BaseModel):
    name: str
    description: Optional[str]
    externalDocs: Optional[ExternalDoc]

    class Config:
        extra = "allow"


class Reference(BaseModel):
    ref: str = Field(..., alias="$ref")


class Schema(BaseModel):
    # Fixed fields in AsyncAPI spec
    discriminator: Optional[str]
    externalDocs: Optional[ExternalDoc]
    deprecated: Optional[bool]
    # Fields from IETF JSON schema validation
    # https://datatracker.ietf.org/doc/html/draft-handrews-json-schema-validation-01
    # TODO: review these more closely
    title: Optional[str]
    type: Optional[str]
    multipleOf: Optional[float]
    maximum: Optional[float]
    exclusiveMaximum: Optional[float]
    minimum: Optional[float]
    exclusiveMinimum: Optional[float]
    maxLength: Optional[int] = Field(None, gte=0)
    minLength: Optional[int] = Field(None, gte=0)
    pattern: Optional[str]
    maxItems: Optional[int] = Field(None, gte=0)
    minItems: Optional[int] = Field(None, gte=0)
    uniqueItems: Optional[bool]
    maxProperties: Optional[int] = Field(None, gte=0)
    minProperties: Optional[int] = Field(None, gte=0)
    required: Optional[List[str]]
    enum: Optional[List[Any]]
    allOf: Optional[List["Schema"]]
    oneOf: Optional[List["Schema"]]
    anyOf: Optional[List["Schema"]]
    not_: Optional["Schema"] = Field(None, alias="not")
    items: Optional["Schema"]
    properties: Optional[Dict[str, "Schema"]]
    additionalProperties: Optional[Union["Schema", Reference, bool]]
    description: Optional[str]
    format: Optional[str]
    default: Optional[Any]
    nullable: Optional[bool]
    readOnly: Optional[bool]
    writeOnly: Optional[bool]
    example: Optional[Any]

    class Config:
        extra: str = "allow"


class Contact(BaseModel):
    name: Optional[str]
    url: Optional[AnyUrl]
    email: Optional[str]
    # ^^ TODO: consider Optional[EmailStr]
    # was email-validator.py having problems in other apps?

    class Config:
        extra = "allow"


class License(BaseModel):
    name: str
    url: Optional[AnyUrl]

    class Config:
        extra = "allow"


class Info(BaseModel):
    title: str
    version: str
    description: Optional[str]
    termsOfService: Optional[AnyUrl]
    contact: Optional[Contact]
    license: Optional[License]

    class Config:
        extra = "allow"


# AsyncAPI auth is the same as OpenAPI auth
# Security code taken from FastAPI openapi.models
class SecuritySchemeType(Enum):
    apiKey = "apiKey"
    http = "http"
    oauth2 = "oauth2"
    openIdConnect = "openIdConnect"


class SecurityBase(BaseModel):
    type_: SecuritySchemeType = Field(..., alias="type")
    description: Optional[str] = None

    class Config:
        extra = "allow"


class APIKeyIn(Enum):
    query = "query"
    header = "header"
    cookie = "cookie"


class APIKey(SecurityBase):
    type_ = Field(SecuritySchemeType.apiKey, alias="type")
    in_: APIKeyIn = Field(..., alias="in")
    name: str


class HTTPBase(SecurityBase):
    type_ = Field(SecuritySchemeType.http, alias="type")
    scheme: str


class HTTPBearer(HTTPBase):
    scheme = "bearer"
    bearerFormat: Optional[str] = None


class OAuthFlow(BaseModel):
    refreshUrl: Optional[str] = None
    scopes: Dict[str, str] = {}

    class Config:
        extra = "allow"


class OAuthFlowImplicit(OAuthFlow):
    authorizationUrl: str


class OAuthFlowPassword(OAuthFlow):
    tokenUrl: str


class OAuthFlowClientCredentials(OAuthFlow):
    tokenUrl: str


class OAuthFlowAuthorizationCode(OAuthFlow):
    authorizationUrl: str
    tokenUrl: str


class OAuthFlows(BaseModel):
    implicit: Optional[OAuthFlowImplicit] = None
    password: Optional[OAuthFlowPassword] = None
    clientCredentials: Optional[OAuthFlowClientCredentials] = None
    authorizationCode: Optional[OAuthFlowAuthorizationCode] = None

    class Config:
        extra = "allow"


class OAuth2(SecurityBase):
    type_ = Field(SecuritySchemeType.oauth2, alias="type")
    flows: OAuthFlows


class OpenIdConnect(SecurityBase):
    type_ = Field(SecuritySchemeType.openIdConnect, alias="type")
    openIdConnectUrl: str


SecurityScheme = Union[APIKey, HTTPBase, OAuth2, OpenIdConnect, HTTPBearer]


class SecurityRequirement(BaseModel):
    name: Optional[List[str]]


class ServerVariable(BaseModel):
    enum: Optional[List[str]]
    default: Optional[str]
    description: Optional[str]
    examples: Optional[List[str]]

    class Config:
        extra = "allow"


class Server(BaseModel):
    url: AnyUrl
    protocol: str
    protocolVersion: Optional[str]
    description: Optional[str]
    variables: Optional[Dict[str, ServerVariable]]
    security: Optional[List[SecurityRequirement]]
    bindings: Optional[List[Union[ServerBinding, Reference]]]

    def validate_protocol(cls, v):
        assert v in VALID_PROTOCOLS
        return v

    class Config:
        extra = "allow"


class OperationTrait(BaseModel):
    operationId: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDoc]
    bindings: Optional[Dict[str, Union[OperationBinding, Reference]]]

    class Config:
        extra = "allow"


class CorrelationId(BaseModel):
    description: Optional[str]
    location: str


class MessageExample(BaseModel):
    headers: Optional[Dict[str, Any]]
    payload: Optional[Any]
    name: Optional[str]
    summary: Optional[str]

    class Config:
        extra = "allow"


class MessageTrait(BaseModel):
    headers: Optional[Union[Schema, Reference]]
    correlationId: Optional[Union[CorrelationId, Reference]]
    schemaFormat: Optional[str]
    contentType: Optional[str]
    name: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDoc]
    bindings: Optional[Dict[str, Union[MessageBinding, Reference]]]
    examples: Optional[List[MessageExample]]

    class Config:
        extra = "allow"


class Message(BaseModel):
    headers: Optional[Dict[str, Union[Schema, Reference]]]
    payload: Optional[Any]
    correlationId: Optional[Union[CorrelationId, Reference]]
    schemaFormat: Optional[str]
    contentType: Optional[str]
    name: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDoc]
    bindings: Optional[Dict[str, Union[MessageBinding, Reference]]]
    examples: Optional[List[MessageExample]]
    traits: Optional[List[Union[MessageTrait, Reference]]]


class Operation(BaseModel):
    operationId: Optional[str]
    summary: Optional[str]
    description: Optional[str]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDoc]
    bindings: Optional[Dict[str, Union[OperationBinding, Reference]]]
    traits: Optional[List[Union[OperationTrait, Reference]]]
    message: Optional[Dict[str, Union[Message, Reference]]]


class Parameter(BaseModel):
    description: Optional[str]
    schema_: Optional[Union[Schema, Reference]] = Field(default=None, alias="schema")
    location: Optional[str]


class Channel(BaseModel):
    ref: str = Field(..., alias="$ref")
    description: Optional[str]
    servers: Optional[List[Server]]
    subscribe: Optional[Operation]
    publish: Optional[Operation]
    parameters: Optional[List[Parameter]]
    bindings: Optional[Dict[ChannelBinding, Reference]]

    class Config:
        extra = "allow"


class Components(BaseModel):
    schemas: Optional[Dict[str, Union[Schema, Reference]]]
    messages: Optional[Dict[str, Union[Message, Reference]]]
    securitySchemas: Optional[Dict[str, Union[SecurityScheme, Reference]]]
    parameters: Optional[Dict[str, Union[Parameter, Reference]]]
    correlationIds: Optional[Dict[str, Union[CorrelationId, Reference]]]
    operationTraits: Optional[Dict[str, Union[OperationTrait, Reference]]]
    messageTraits: Optional[Dict[str, Union[MessageTrait, Reference]]]
    serverBindings: Optional[Dict[str, Union[ServerBinding, Reference]]]
    channelBindings: Optional[Dict[str, Union[ChannelBinding, Reference]]]
    operationBindings: Optional[Dict[str, Union[OperationBinding, Reference]]]
    messageBindings: Optional[Dict[str, Union[MessageBinding, Reference]]]

    class Config:
        extra = "allow"


class AsyncAPI(BaseModel):
    asyncapi: str
    id: Optional[str]
    info: Info
    servers: Optional[List[Server]]
    defaultContentType: Optional[str]
    channels: Dict[str, Channel]
    components: Optional[Components]
    tags: Optional[List[Tag]]
    externalDocs: Optional[ExternalDoc]

    class Config:
        extra = "allow"
