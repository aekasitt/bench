#!/usr/bin/env python3.13
"""
Type stubs for starlette for JSONResponse, PlainTextResponse, Response
"""

### Standard packages ###
from typing import Any, Final, Mapping


class Response:
  media_type: None | str = None
  charset: str = "utf-8"

  def __init__(
    self,
    content: bytes | str | memoryview,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    media_type: None | str = None
  ) -> None:
    ...


class JSONResponse(Response):
  media_type = "application/json"

  def __init__(
    self,
    content: Any,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    media_type: None | str = None
  ) -> None:
    ...


class PlainTextResponse(Response):
  media_type = "text/plain"


__all__: Final[tuple[str, ...]] = ("Response", "JSONResponse", "PlainTextResponse")
