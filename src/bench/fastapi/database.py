#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/fastapi/database.py
# VERSION:     0.1.0
# CREATED:     2025-01-22 15:23
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from contextlib import asynccontextmanager
from logging import Logger, getLogger
from typing import AsyncGenerator, ClassVar, Final

### Third-party packages ###
from asyncpg import Connection, Pool, create_pool
from asyncpg.exceptions import PostgresError
from starlette.requests import Request
from starlette.responses import Response

### Local modules ###
from bench.fastapi.configs import POSTGRES_POOL_SIZE, POSTGRES_URI

### Initiate module logger ###
logger: Logger = getLogger("uvicorn")


class PostgresPool:
  pool: ClassVar[Pool]

  def __init__(self) -> None:
    raise NotImplementedError("PostgresPool can only be initiated with init method")

  @classmethod
  def init(cls, workers: int = 1) -> None:
    try:
      cls.pool = await create_pool(
        POSTGRES_URI,
        max_inactive_connection_lifetime=5,
        max_size=POSTGRES_POOL_SIZE // workers,
        min_size=1,
      )
    except PostgresError as e:
      logger.error(f"Error creating PostgreSQL connection pool: {e}")
      raise ValueError("Failed to create PostgreSQL connection pool")

  @classmethod
  async def close(cls) -> None:
    if cls.pool is not None:
      await cls.pool.close()


class Postgres:
  def __call__(self, request: Request, response: Response) -> "Postgres":
    if PostgresPool.pool is None:
      logger.exception("Please initiate PostgresPool during FastAPI startup")
    return self

  @asynccontextmanager
  async def acquire(self) -> AsyncGenerator[Connection, None]:
    async with PostgresPool.pool.acquire() as connection:
      yield connection


__all__: Final[tuple[str, ...]] = ("Postgres", "PostgresPool")
