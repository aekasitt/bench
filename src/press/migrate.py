#!/usr/bin/env python3.12
"""
Migration script for databases used in tests
"""

### Standard packages ###
from asyncio import AbstractEventLoop, get_event_loop

### Third-party packages ###
from asyncpg import Connection, connect
from asyncpg.exceptions import PostgresError

### Local modules ###
from bench_uvicorn.configs import POSTGRES_URI


async def create_database() -> None:
  """
  """
  try:
    connection: Connection = await connect(POSTGRES_URI)
    table_drops: tuple[str, ...] = (
      "DROP TABLE IF EXISTS fastapi_device;",
      "DROP TABLE IF EXISTS fastify_device;",
      "DROP TABLE IF EXISTS litestar_device;",
      "DROP TABLE IF EXISTS vanilla_device;",
      "DROP TABLE IF EXISTS uvicorn_device;",
    )
    for drop in map(connection.execute, table_drops):
      result: str = await drop
      print(f"Create result: { result }")
    table_creates: tuple[str, ...] = ( 
       """
       CREATE TABLE IF NOT EXISTS fastapi_device (
         id SERIAL PRIMARY KEY,
         uuid UUID DEFAULT NULL,
         mac VARCHAR(255) DEFAULT NULL,
         firmware VARCHAR(255) DEFAULT NULL,
         created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
         updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
       );
       """,
       """
       CREATE TABLE IF NOT EXISTS fastify_device (
         id SERIAL PRIMARY KEY,
         uuid UUID DEFAULT NULL,
         mac VARCHAR(255) DEFAULT NULL,
         firmware VARCHAR(255) DEFAULT NULL,
         created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
         updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
       );
       """,
       """
       CREATE TABLE IF NOT EXISTS litestar_device (
         id SERIAL PRIMARY KEY,
         uuid UUID DEFAULT NULL,
         mac VARCHAR(255) DEFAULT NULL,
         firmware VARCHAR(255) DEFAULT NULL,
         created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
         updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
       );
       """,
       """
       CREATE TABLE IF NOT EXISTS vanilla_device (
         id SERIAL PRIMARY KEY,
         uuid UUID DEFAULT NULL,
         mac VARCHAR(255) DEFAULT NULL,
         firmware VARCHAR(255) DEFAULT NULL,
         created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
         updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
       );
       """,
       """
       CREATE TABLE IF NOT EXISTS uvicorn_device (
         id SERIAL PRIMARY KEY,
         uuid UUID DEFAULT NULL,
         mac VARCHAR(255) DEFAULT NULL,
         firmware VARCHAR(255) DEFAULT NULL,
         created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
         updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
       );
       """,
    )
    for create in map(connection.execute, table_creates):
      result: str = await create
      print(f"Create result: { result }")
  except PostgresError as err:
    print(err)


def main() -> None:
  loop: AbstractEventLoop = get_event_loop()
  loop.run_until_complete(create_database())


if __name__ == "__main__":
  main()


__all__: tuple[str, ...] = ("create_database",)
