#!/usr/bin/env python3.13
"""
Type stubs for litestar exceptions module.
"""

### Standard packages ###
from typing import Any

class HTTPException(Exception):
  """HTTP exception for Litestar."""

  def __init__(
    self,
    status_code: int,
    detail: str | None = None,
    headers: dict[str, str] | None = None,
    **kwargs: Any,
  ) -> None: ...
  @property
  def status_code(self) -> int: ...
  @property
  def detail(self) -> str | None: ...
  @property
  def headers(self) -> dict[str, str] | None: ...

class ValidationException(HTTPException):
  """Validation exception."""

  pass

class NotFoundException(HTTPException):
  """Not found exception."""

  pass

class MethodNotAllowedException(HTTPException):
  """Method not allowed exception."""

  pass

__all__: tuple[str, ...] = (
  "HTTPException",
  "ValidationException",
  "NotFoundException",
  "MethodNotAllowedException",
)
