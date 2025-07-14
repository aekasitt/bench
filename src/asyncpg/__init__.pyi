#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/asyncpg/__init__.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-26 12:49
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************
"""
Type stubs for asyncpg package main module.
"""

### Standard packages ###
from typing import Any, Final

### Local modules ###
from asyncpg.connection import Connection, connect
from asyncpg.protocol.protocol import Record


class Pool:
  """A connection pool."""

  def acquire(self) -> "PoolAcquireContext":
    """Acquire a database connection from the pool."""

  async def close(self) -> None:
    """Attempt to gracefully close all connections in the pool."""


class PoolAcquireContext:
  """A pool connection acquiring context."""

  __slots__ = ("timeout", "connection", "done", "pool")

  async def __aenter__(self) -> Connection:
    ...

  async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
    ...


def create_pool(
  dsn: str,
  *,
  min_size: int = 10,
  max_size: int = 10,
  max_inactive_connection_lifetime: float = 300.0,
  **kwargs: Any,
) -> Pool:
  """Create a connection pool."""


__all__: Final[tuple[str, ...]] = (
  "Connection",
  "Record",
  "Pool",
  "PoolAcquireContext",
  "create_pool",
  "connect",
)
