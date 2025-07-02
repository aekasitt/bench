#!/usr/bin/env python3.12
"""
Type stubs for pymemcache base Client
"""

from typing import Any

Key = bytes | str


class Client:
  def __init__(
    self,
    servers: list[str],
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

  def disconnect_all(self) -> None:
    """Disconnect from all servers and reset state."""

  def get(self, key: bytes | str) -> None | bytes:
    """TODO"""

  def get_behaviors(self) -> dict[str, int]:
    """TODO"""

  def get_stats(self) -> list[tuple[bytes, dict[bytes, Any]]]:
    """TODO"""

  def set(
    self, key: Key, value: str, time: int = 0, min_compress_len: int = 0, compress_level: int = -1
  ) -> bool:
    """TODO"""


__all__: tuple[str, ...] = ("Client",)
