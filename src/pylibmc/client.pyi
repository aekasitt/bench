#!/usr/bin/env python3.12
"""
Type stubs for pymemcache base Client
"""

from typing import Any


class Client:
  def __init__(
    self,
    server: str,
    behaviors: None | dict[str, str] = None,
    binary: bool = False,
    username: None | str = None,
    password: None | str = None,
  ) -> None:
    """TODO"""

  def clone(self) -> None:
    """TODO"""

  def delete(self, key: bytes) -> bool:
    """TODO"""

  def get(self, key: bytes | str) -> None | bytes:
    """TODO"""

  def get_behaviors(self) -> dict[str, int]:
    """TODO"""

  def get_stats(self, obj: Any) -> tuple[tuple[str, Any], ...]:
    """TODO"""

  def set(self, key: bytes | str, value: bytes, exptime: int = 0, flags: int = 0) -> bool:
    """TODO"""


__all__: tuple[str, ...] = ("Client",)
