#!/usr/bin/env python3.12
"""
Type stubs for uvicorn _types package.
"""

### Standard packages ###
from collections.abc import Awaitable, Iterable
from typing import Any, Callable, Literal, NotRequired, Protocol, TypedDict


class ASGIReceiveEvent(TypedDict):
  type: Literal["http.disconnect", "http.request"]
  body: bytes
  more_body: bool


class ASGISendEvent(TypedDict):
  body: NotRequired[bytes]
  type: Literal["http.response.body", "http.response.start"]
  status: NotRequired[int]
  headers: NotRequired[Iterable[tuple[bytes, bytes]]]
  trailers: NotRequired[bool]
  more_body: NotRequired[bool]


class ASGIVersions(TypedDict):
  spec_version: str
  version: Literal["2.0"] | Literal["3.0"]


class Scope(TypedDict):
  type: Literal["http"]
  asgi: ASGIVersions
  http_version: str
  method: str
  scheme: str
  path: str
  raw_path: bytes
  query_string: bytes
  root_path: str
  headers: Iterable[tuple[bytes, bytes]]
  client: tuple[str, int] | None
  server: tuple[str, int | None] | None
  state: NotRequired[dict[str, Any]]
  extensions: NotRequired[dict[str, dict[object, object]]]


ASGIReceiveCallable = Callable[[], Awaitable[ASGIReceiveEvent]]
ASGISendCallable = Callable[[ASGISendEvent], Awaitable[None]]


class ASGI2Protocol(Protocol):
  def __init__(self, scope: Scope) -> None:
    """TODO"""

  async def __call__(self, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
    """TODO"""


ASGI2Application = type[ASGI2Protocol]
ASGI3Application = Callable[[Scope, ASGIReceiveCallable, ASGISendCallable], Awaitable[None]]
ASGIApplication = ASGI2Application | ASGI3Application


__all__: tuple[str, ...] = (
  "ASGIApplication",
  "ASGIReceiveCallable",
  "ASGIReceiveEvent",
  "ASGISendCallable",
  "ASGISendEvent",
  "Scope"
)
