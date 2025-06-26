"""
Type stubs for aiomcache package.
"""

from typing import Any, Dict


class Client:
  def __init__(
      self,
      host: str = "127.0.0.1",
      port: int = 11211,
      pool_size: int = 10,
      **kwargs: Any
  ) -> None:
    """TODO"""

  async def set(
      self,
      key: bytes,
      value: bytes,
      exptime: int = 0,
      flags: int = 0
  ) -> bool:
    """TODO"""

  async def get(self, key: bytes) -> None | bytes:
    """TODO"""
  async def delete(self, key: bytes) -> bool:
    """TODO"""
  async def stats(self) -> Dict[bytes, bytes]:
    """TODO"""
  async def close(self) -> None:
    """TODO"""


__all__: tuple[str, ...] = ("Client",)
