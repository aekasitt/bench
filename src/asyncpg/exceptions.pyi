#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/asyncpg/exceptions.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-26 12:49
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

class PostgresMessageMeta(type):
  def __instancecheck__(cls, instance: "PostgresMessage") -> bool:
    """TODO"""

class PostgresMessage(metaclass=PostgresMessageMeta):
  """TODO"""

class PostgresError(PostgresMessage, Exception):
  """TODO"""

__all__: tuple[str, ...] = ("PostgresError", "PostgresMessage", "PostgresMessageMeta")
