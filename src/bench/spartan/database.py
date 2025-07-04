#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/spartan/database.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from types import TracebackType
from typing import Type, Final

### Third-party packages ###
from asyncpg import Connection, connect

### Local modules ###
from bench.spartan.configs import POSTGRES_URI


class Postgres:
  connection: Connection

  async def __aenter__(self) -> "Postgres":
    self.connection = await connect(POSTGRES_URI)
    return self

  async def __aexit__(
    self, exc_type: None | Type[BaseException], exc: Type[BaseException], tb: TracebackType
  ) -> None:
    # del self.connection
    ...


__all__: Final[tuple[str, ...]] = ("Postgres",)
