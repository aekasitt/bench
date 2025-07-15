#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/asyncpg/connection.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-28 01:45
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any

### Local modules ###
from asyncpg.protocol.protocol import Record


class ConnectionMeta(type):
  def __instancecheck__(cls, instance: "Connection") -> bool:
    """TODO"""


class Connection(metaclass=ConnectionMeta):
  """TODO"""
  async def fetchrow(
    self, query: str, *args: Any, timeout: None | float = None, record_class: None | "Record" = None
  ) -> "Record":
    """TODO"""
  async def fetch(self, query: str, *args: Any) -> list["Record"]:
    """TODO"""
  async def execute(self, query: str, *args: Any) -> str:
    """TODO"""
  async def close(self) -> None:
    """TODO"""


async def connect(dsn: str, **kwargs: Any) -> Connection:
  """TODO"""


__all__: tuple[str, ...] = ("Connection", "ConnectionMeta", "connect")
