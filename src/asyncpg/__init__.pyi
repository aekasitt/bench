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
from typing import Any, Union, overload

class ConnectionMeta(type):
  def __instancecheck__(cls, instance: "Connection") -> bool:
    """TODO"""

class Connection(metaclass=ConnectionMeta):
  """TODO"""
  async def fetchrow(
    self, query: str, *args: Any, timeout: None | float = None, record_class: None | "Record" = None
  ) -> "Record": ...
  async def fetch(self, query: str, *args: Any) -> list["Record"]: ...
  async def execute(self, query: str, *args: Any) -> str: ...
  async def close(self) -> None: ...

class Record:
  """TODO"""

  @overload
  def __getitem__(self, index: str) -> Any: ...
  @overload
  def __getitem__(self, index: int) -> Any: ...
  @overload
  def __getitem__(self, index: slice) -> tuple[Any, ...]: ...
  def get(self, key: Union[str, int], default: Any = None) -> Any: ...

class Pool:
  """TODO"""

  def acquire(self) -> "PoolAcquireContext": ...
  async def close(self) -> None: ...

class PoolAcquireContext:
  """TODO"""

  async def __aenter__(self) -> Connection: ...
  async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...

def create_pool(
  dsn: str,
  *,
  min_size: int = 10,
  max_size: int = 10,
  max_inactive_connection_lifetime: float = 300.0,
  **kwargs: Any,
) -> Pool:
  """TODO"""

async def connect(dsn: str, **kwargs: Any) -> Connection: ...

__all__: tuple[str, ...] = (
  "Connection",
  "ConnectionMeta",
  "Record",
  "Pool",
  "create_pool",
  "connect",
)
