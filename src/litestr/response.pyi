#!/usr/bin/env python3.13
"""
Type stubs for litestar response module.
"""

### Standard packages ###
from typing import Any, Generic, TypeVar

### Type variables ###
T = TypeVar("T")

class Response(Generic[T]):
  """Response class for Litestar."""

  def __init__(
    self,
    content: T,
    status_code: int = 200,
    media_type: str | None = None,
    headers: dict[str, str] | None = None,
    **kwargs: Any,
  ) -> None: ...
  @property
  def content(self) -> T: ...
  @property
  def status_code(self) -> int: ...
  @property
  def media_type(self) -> str | None: ...
  @property
  def headers(self) -> dict[str, str] | None: ...

class JSONResponse(Response[dict[str, Any]]):
  """JSON response for Litestar."""

  pass

class PlainTextResponse(Response[str]):
  """Plain text response for Litestar."""

  pass

class HTMLResponse(Response[str]):
  """HTML response for Litestar."""

  pass

__all__: tuple[str, ...] = (
  "Response",
  "JSONResponse",
  "PlainTextResponse",
  "HTMLResponse",
)
