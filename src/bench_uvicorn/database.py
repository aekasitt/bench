#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_starlette/database.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from logging import Logger, getLogger

### Third-party packages ###
from asyncpg import Connection, connect
from asyncpg.exceptions import PostgresError

### Local modules ###
from bench_uvicorn.configs import POSTGRES_URI

### Initiate module logger ###
logger: Logger = getLogger(__name__)


async def get_database() -> Connection:
  """Get a database connection"""
  try:
    connection = await connect(POSTGRES_URI)
    logger.info("Database connection created")
    return connection
  except PostgresError as e:
    logger.error(f"Error creating PostgreSQL connection: {e}")
    raise ValueError("Failed to create PostgreSQL connection")


async def get_postgres_connection() -> Connection:
  """Get PostgreSQL connection instance"""
  return await get_database()


__all__ = ("get_database", "get_postgres_connection")
