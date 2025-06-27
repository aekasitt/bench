#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/asyncpg/protocol/protocol.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-28 01:45
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Dict, overload

BUILTIN_TYPE_NAME_MAP: Dict[str, Any]
NO_TIMEOUT: float = 0.0


class Protocol:
  """PostgreSQL protocol implementation."""

  def __init__(self, **kwargs: Any) -> None:
    """TODO"""
  async def connect(self, **kwargs: Any) -> None:
    """TODO"""
  async def close(self) -> None:
    """TODO"""
  async def execute(self, query: str, *args: Any, **kwargs: Any) -> Any:
    """TODO"""
  async def fetch(self, query: str, *args: Any, **kwargs: Any) -> list["Record"]:
    """TODO"""
  async def fetchrow(self, query: str, *args: Any, **kwargs: Any) -> "Record" | None:
    """TODO"""


class Record:
  """TODO"""

  @overload
  def __getitem__(self, index: str) -> Any:
    """index getitem"""
  @overload
  def __getitem__(self, index: int) -> Any:
    """index getitem"""
  @overload
  def __getitem__(self, index: slice) -> tuple[Any, ...]:
    """index getitem"""

  def get(self, key: int | str, default: Any = None) -> Any:
    """TODO"""


__all__: tuple[str, ...] = ("Protocol", "Record", "NO_TIMEOUT", "BUILTIN_TYPE_NAME_MAP")
