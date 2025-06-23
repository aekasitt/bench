#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_litestar/database.py
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
from typing import AsyncGenerator

### Third-party packages ###
from asyncpg import Connection, Pool, create_pool
from asyncpg.exceptions import PostgresError

### Local modules ###
from bench_litestar.configs import POSTGRES_POOL_SIZE, POSTGRES_URI

### Initiate module logger ###
logger: Logger = getLogger(__name__)

@asynccontextmanager
async def get_database() -> AsyncGenerator[Connection, None]:
  pool: None | Pool = None
  try:
    pool = await create_pool(
      POSTGRES_URI,
      min_size=10,
      max_size=POSTGRES_POOL_SIZE,
      max_inactive_connection_lifetime=300,
    )
    logger.info("Database pool created: %s", pool)
    async with pool.acquire() as connection:
      yield connection
  except PostgresError as e:
    logger.error(f"Error creating PostgreSQL connection pool: {e}")
    raise ValueError("Failed to create PostgreSQL connection pool")
  finally:
    if pool is not None:
      await pool.close()


async def get_postgres_connection() -> Connection:
  """Dependency for getting PostgreSQL connection"""
  async with get_database() as connection:
    yield connection

__all__ = ("get_database", "get_postgres_connection") 