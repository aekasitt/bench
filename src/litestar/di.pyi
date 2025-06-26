#!/usr/bin/env python3.13
"""
Type stubs for litestar dependency injection module.
"""

### Standard packages ###
from typing import Any, Callable, TypeVar

### Type variables ###
T = TypeVar("T")

class Provide:
  """Dependency provider for Litestar."""

  def __init__(
    self,
    dependency: Callable[..., T],
    **kwargs: Any,
  ) -> None: ...
  @property
  def dependency(self) -> Callable[..., T]: ...

__all__: tuple[str, ...] = ("Provide",)
