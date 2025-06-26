#!/usr/bin/env python3.13
"""
Type stubs for litestar package main module.
"""

### Standard packages ###
from typing import Any, Callable, TypeVar

### Type variables ###
F = TypeVar("F", bound=Callable[..., Any])

### Classes ###
class Litestar:
  def __init__(
    self,
    route_handlers: list[Callable[..., Any]] | None = None,
    dependencies: dict[str, Any] | None = None,
    **kwargs: Any,
  ) -> None: ...

### Decorators ###
def get(
  path: str,
  status_code: int = 200,
  sync_to_thread: bool = True,
  **kwargs: Any,
) -> Callable[[F], F]: ...
def post(
  path: str,
  status_code: int = 201,
  sync_to_thread: bool = True,
  **kwargs: Any,
) -> Callable[[F], F]: ...
def put(
  path: str,
  status_code: int = 200,
  sync_to_thread: bool = True,
  **kwargs: Any,
) -> Callable[[F], F]: ...
def delete(
  path: str,
  status_code: int = 204,
  sync_to_thread: bool = True,
  **kwargs: Any,
) -> Callable[[F], F]: ...
def patch(
  path: str,
  status_code: int = 200,
  sync_to_thread: bool = True,
  **kwargs: Any,
) -> Callable[[F], F]: ...

__all__: tuple[str, ...] = ("Litestar", "get", "post", "put", "delete", "patch")
