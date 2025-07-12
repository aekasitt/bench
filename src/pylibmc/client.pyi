#!/usr/bin/env python3.12
"""
Type stubs for pymemcache base Client
"""

### Standard packages ###
from __future__ import annotations
from typing import Any, Final, Mapping, Sequence

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
    """Initialize a memcached client instance."""

  def clone(self) -> None:
    """Clone this client entirely such that it is safe to access from
    another thread. This creates a new connection.
    """

  def delete(self, key: Key) -> bool:
    """Delete a key."""

  def disconnect_all(self) -> None:
    """Disconnect from all servers and reset state."""

  def get(self, key: Key) -> None | bytes:
    """Retrieve a key from a memcached."""

  def get_multi(keys: Sequence[Key], key_prefix: None | Key = None) -> Sequence[Any]:
    """Get multiple keys at once."""

  def get_stats(self) -> list[tuple[bytes, dict[bytes, Any]]]:
    """Retrieve statistics from all memcached servers"""

  def set(
    self, key: Key, value: str, time: int = 0, min_compress_len: int = 0, compress_level: int = -1
  ) -> bool:
    """Set a key unconditionally."""

  def set_multi(
    keys: Mapping[Key, Any], time: int = 0, min_compress_len: int = 0, compress_level: int = -1
  ) -> list[Key]:
    """Set multiple keys at once."""

  def touch(self, key: Key, ttl: int = 0) -> None:
    """Change the TTL of a key."""


__all__: Final[tuple[str, ...]] = ("Client",)
