#!/usr/bin/env python3.13
"""
Type stubs for msgspec.json package
"""

from __future__ import annotations
from typing import Any, Callable, Final, Literal


def decode(
  buf: None | bytes | bytearray | memoryview | str,
  *,
  type: None | type = None,
  strict: None | bool = None,
  dec_hook: Callable[[], None] | None = None
) -> Any:
  """
  Deserialize an object from JSON

  ---
  :raises TypeError:
  """


def encode(
  obj: Any,
  *,
  enc_hook: None | Callable[[], None] = None,
  order: None | Literal["deterministic", "sorted"] = None,
) -> bytes:
  """
  Serialize an object as JSON
  """


__all__: Final[tuple[str, ...]] = ("decode", "encode")
