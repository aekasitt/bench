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

### Standard packages ###
from typing import Any, Awaitable, Coroutine, overload


class ConnectionMeta(type):
  def __instancecheck__(cls, instance: "Connection") -> bool:
    """TODO"""


class Connection(metaclass=ConnectionMeta):
  """TODO"""
  async def fetchrow(
    self,
    query: str,
    *args: Any,
    timeout: None | float = None,
    record_class: None | "Record" = None
  ) -> "Record":
    ...


class Record:
  """TODO"""

  @overload
  def __getitem__(self, index: str) -> Any:
    ...

  @overload
  def __getitem__(self, index: int) -> Any:
    ...

  @overload
  def __getitem__(self, index: slice) -> tuple[Any, ...]:
    ...


class Pool:
  """TODO"""

  def acquire(self, *, timeout: None | float = None) -> "PoolAcquireContext":
    ...

  async def close(self) -> None:
    ...


class PoolAcquireContext:
  """TODO"""

  async def __aenter__(self) -> Connection:
    ...

  async def __aexit__(self, *exc: Any) -> None:
    ...


def create_pool(
  dsn: None | str = None,
  *,
  min_size: int = 10,
  max_size: int = 10,
  max_queries: int = 50000,
  max_inactive_connection_lifetime: float = 300.0,
  connect: Coroutine[None, None, Any] | None = None,
  setup: Coroutine[None, None, Any] | None = None,
  init: Coroutine[None, None, Any] | None = None,
  reset: Coroutine[None, None, Any] | None = None,
  loop: Coroutine[None, None, Any] | None = None,
  connection_class:type = Connection,
  record_class: type = Record,
  **connect_kwargs: Any,
) -> Awaitable[Pool]:
  """TODO"""


__all__: tuple[str, ...] = ("Connection", "ConnectionMeta", "Record", "Pool", "create_pool")
