#!/usr/bin/env python3.12
"""
Type stubs for pymemcache base Client
"""

from typing import Any


class Client:
  def __init__(
    self, host: str = "127.0.0.1", port: int = 11211, pool_size: int = 10, **kwargs: Any
  ) -> None:
    """TODO"""

  def cache_memlimit(self, memlimit: int) -> bool:
    """The memcached "cache_memlimit" command."""

  def delete(self, key: bytes) -> bool:
    """TODO"""

  def set(self, key: bytes | str, value: bytes, exptime: int = 0, flags: int = 0) -> bool:
    """TODO"""

  def get(self, key: bytes | str) -> None | bytes:
    """TODO"""

  def stats(self) -> dict[bytes, bytes]:
    """The memcached "stats" command."""

  def close(self) -> None:
    """TODO"""


__all__: tuple[str, ...] = ("Client",)
