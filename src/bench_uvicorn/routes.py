#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_starlette/routes.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from dataclasses import dataclass
from datetime import datetime, timezone
from json import JSONDecodeError, dumps, loads
from logging import Logger, getLogger
from socket import gaierror as SocketError
from time import perf_counter
from typing import Any
from uuid import UUID, uuid4 as uuid

### Third-party packages ###
# from uvicorn._types import HTTPScope, ASGIReceiveCallable, ASGISendCallable
from asyncpg.exceptions import PostgresError

### Local modules ###
from bench_uvicorn.cache import Memcached
from bench_uvicorn.database import Postgres
from bench_uvicorn.metrics import H

### Initiate module logger ###
logger: Logger = getLogger("uvicorn")


@dataclass
class Device:
  firmware: str
  mac: str

  @classmethod
  def from_bytes(cls, data: bytes) -> "Device":
    str_repr: str = data.decode("utf-8")
    dict_repr: dict[str, Any] = loads(str_repr)
    return Device(**dict_repr)


H_MEMCACHED_LABEL = H.labels(op="set", db="memcache")
H_POSTGRES_LABEL = H.labels(op="insert", db="postgres")


async def create_device(scope: Any, receive: Any, send: Any) -> None:
  body: bytes = b""
  more_body: bool = True
  while more_body:
    message: dict[str, Any] = await receive()
    assert message["type"] == "http.request"
    body += message.get("body", b"")
    more_body = message.get("more_body", False)
  try:
    device: Device = Device.from_bytes(body)
    now = datetime.now(timezone.utc)
    device_uuid: UUID = uuid()
    insert_query = """
            INSERT INTO uvicorn_device (uuid, mac, firmware, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id;
            """
    start_time: float = perf_counter()
    async with Postgres() as postgres:
      row = await postgres.connection.fetchrow(
        insert_query, device_uuid, device.mac, device.firmware, now, now
      )
      H_POSTGRES_LABEL.observe(perf_counter() - start_time)
      if not row:
        await send(
          {
            "type": "http.response.start",
            "status": 500,
            "headers": [(b"Content-Type", b"text/plain")],
          }
        )
        await send(
          {
            "type": "http.response.body",
            "body": b"Failed to create device record",
          }
        )
        return
    device_dict = {
      "id": row["id"],
      "uuid": str(device_uuid),
      "mac": device.mac,
      "firmware": device.firmware,
      "created_at": now.isoformat(),  #
      "updated_at": now.isoformat(),
    }
    # Measure cache operation
    start_time = perf_counter()
    with Memcached() as memcached:
      memcached.client.set(
        device_uuid.hex.encode(),
        dumps(device_dict),
        time=20,
      )
    H_MEMCACHED_LABEL.observe(perf_counter() - start_time)
    await send(
      {
        "type": "http.response.start",
        "status": 201,
        "headers": [(b"Content-Type", b"application/json")],
      }
    )
    await send(
      {
        "type": "http.response.body",
        "body": dumps(device_dict).encode("utf-8"),
      }
    )
  except JSONDecodeError:
    await send(
      {
        "type": "http.response.start",
        "status": 400,
        "headers": [(b"Content-Type", b"text/plain")],
      }
    )
    await send(
      {
        "type": "http.response.body",
        "body": b"Invalid payload",
      }
    )
  except PostgresError:
    logger.exception("Postgres error")
    await send(
      {
        "type": "http.response.start",
        "status": 500,
        "headers": [(b"Content-Type", b"text/plain")],
      }
    )
    await send(
      {
        "type": "http.response.body",
        "body": b"Database error occurred while creating device",
      }
    )
  except (SocketError, ValueError):
    logger.exception("Memcached error")
    await send(
      {
        "type": "http.response.start",
        "status": 500,
        "headers": [(b"Content-Type", b"text/plain")],
      }
    )
    await send(
      {
        "type": "http.response.body",
        "body": b"Memcached Database error occurred while creating device",
      }
    )
  except Exception:
    logger.exception("Unknown error")
    await send(
      {
        "type": "http.response.start",
        "status": 500,
        "headers": [(b"Content-Type", b"text/plain")],
      }
    )
    await send(
      {
        "type": "http.response.body",
        "body": b"An unexpected error occurred while creating device",
      }
    )


async def get_devices(scope: Any, receive: Any, send: Any) -> None:
  """Get static list of devices"""
  devices: tuple[dict[str, int | str], ...] = (
    {
      "id": 1,
      "uuid": "9add349c-c35c-4d32-ab0f-53da1ba40a2a",
      "mac": "EF-2B-C4-F5-D6-34",
      "firmware": "2.1.5",
      "created_at": "2024-05-28T15:21:51.137Z",
      "updated_at": "2024-05-28T15:21:51.137Z",
    },
    {
      "id": 2,
      "uuid": "d2293412-36eb-46e7-9231-af7e9249fffe",
      "mac": "E7-34-96-33-0C-4C",
      "firmware": "1.0.3",
      "created_at": "2024-01-28T15:20:51.137Z",
      "updated_at": "2024-01-28T15:20:51.137Z",
    },
    {
      "id": 3,
      "uuid": "eee58ca8-ca51-47a5-ab48-163fd0e44b77",
      "mac": "68-93-9B-B5-33-B9",
      "firmware": "4.3.1",
      "created_at": "2024-08-28T15:18:21.137Z",
      "updated_at": "2024-08-28T15:18:21.137Z",
    },
  )
  await send(
    {
      "type": "http.response.start",
      "status": 200,
      "headers": [(b"Content-Type", b"application/json")],
    }
  )
  await send(
    {
      "type": "http.response.body",
      "body": dumps(devices).encode("utf-8"),
    }
  )


async def get_device_stats(
  scope: Any,
  receive: Any,
  send: Any,
) -> None:
  try:
    stats: list[tuple[bytes, dict[bytes, Any]]]
    stats_data: dict[str, str] = {}
    with Memcached() as memcached:
      stats = memcached.client.get_stats()
    _, result = stats[0]
    stats_data["bytes"] = str(result.get(b"bytes", 0))
    stats_data["curr_connections"] = result.get(b"curr_connections", 0)
    stats_data["curr_items"] = result.get(b"curr_items", 0)
    stats_data["get_hits"] = result.get(b"get_hits", 0)
    stats_data["get_misses"] = result.get(b"get_misses", 0)
    stats_data["total_items"] = result.get(b"total_items", 0)
    await send(
      {
        "type": "http.response.start",
        "status": 200,
        "headers": [(b"Content-Type", b"application/json")],
      }
    )
    await send(
      {
        "type": "http.response.body",
        "body": dumps(stats_data).encode("utf-8"),
      }
    )
  except (SocketError, ValueError) as e:
    logger.exception(f"Memcached error: {e}")
    await send(
      {
        "type": "http.response.start",
        "status": 500,
        "headers": [(b"Content-Type", b"text/plain")],
      }
    )
    await send(
      {
        "type": "http.response.body",
        "body": b"Memcached error occurred while retrieving stats",
      }
    )
  except Exception as e:
    logger.exception(f"Unknown error: {e}")
    await send(
      {
        "type": "http.response.start",
        "status": 500,
        "headers": [(b"Content-Type", b"text/plain")],
      }
    )
    await send(
      {
        "type": "http.response.body",
        "body": b"An unexpected error occurred while retrieving stats",
      }
    )


async def health(scope: Any, receive: Any, send: Any) -> None:
  """Health check endpoint"""
  await send(
    {
      "type": "http.response.start",
      "status": 200,
      "headers": [(b"Content-Type", b"text/plain")],
    }
  )
  await send(
    {
      "type": "http.response.body",
      "body": b"OK",
    }
  )


__all__: tuple[str, ...] = ("health", "get_devices")
