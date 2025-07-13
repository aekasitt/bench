#!/usr/bin/env python3.12
"""
Type stubs for pylibmc.pools package
"""

### Standard packages ###
from __future__ import annotations
from contextlib import contextmanager
from typing import Final, Generator

### Local modules ###
from pylibmc.client import Client


class ClientPool:
  """Client pooling helper."""

  def __init__(self, mc: Client | None = None, n_slots: int = 0) -> None:
    ...

  @contextmanager
  def reserve(self, block: bool = False) -> Generator[Client, None]:
    """Context manager for reserving a client from the pool.

    If *block* is given and the pool is exhausted, the pool waits for
    another thread to fill it before returning.
    """

  def fill(self, mc: Client, n_slots: int) -> None:
    """Fill n_slots of the pool with clones of mc."""


class ThreadMappedPool:
  """Much like the *ClientPool*, helps you with pooling."""

  def __init__(self, master: Client):
    ...

  def current_key(self) -> None | int:
    ...

  def reserve(self) -> Generator[Client, None]:
    """Reserve a client."""

  def relinquish(self) -> Client:
    """Relinquish any reserved client for the current context."""


__all__: Final[tuple[str, ...]] = ("ClientPool", "ThreadMappedPool")
