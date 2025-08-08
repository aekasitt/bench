#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/spartan/routes.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from fileinput import input
from os import getenv
from socket import gaierror as SocketError
from time import perf_counter
from typing import Any, ClassVar, Final
from uuid import UUID, uuid4 as uuid

### Third-party packages ###
from msgspec.json import decode, encode
from asyncpg import Record, Pool, create_pool
from asyncpg.exceptions import PostgresError
from prometheus_client import Histogram
from pylibmc.client import Client
from pylibmc.pools import ClientPool
from uvicorn._types import ASGIReceiveCallable, ASGIReceiveEvent, ASGISendCallable, Scope

### If development environment, load dotenv ###
try:
  from dotenv import load_dotenv

  load_dotenv(".env")
except ImportError:
  pass

BUCKETS: Final[tuple[float, ...]] = tuple(map(float, input(("buckets.txt",), encoding="utf-8")))
MEMCACHED_HOST: Final[str] = getenv("MEMCACHED_HOST", "127.0.0.1")
MEMCACHED_POOL_SIZE: Final[int] = int(getenv("MEMCACHED_POOL_SIZE", "500"))
POSTGRES_POOL_SIZE: Final[int] = int(getenv("POSTGRES_POOL_SIZE", "20"))
POSTGRES_URI: Final[str] = getenv(
  "POSTGRES_URI", "postgres://bench:benchpwd@localhost:5432/benchdb"
)


@dataclass
class Device:
  firmware: str
  mac: str

  @classmethod
  def from_bytes(cls, data: bytes) -> "Device":
    str_repr: Final[str] = data.decode("utf-8")
    dict_repr: Final[dict[str, str]] = decode(str_repr, type=dict[str, str])
    return Device(**dict_repr)


H: Final[Histogram] = Histogram(
  "myapp_request_duration_seconds",
  "Duration of the request",
  labelnames=("op", "db"),
  buckets=BUCKETS,
)

H_MEMCACHED_LABEL = H.labels(op="set", db="memcache")
H_POSTGRES_LABEL = H.labels(op="insert", db="postgres")


class Memcached:
  pool: ClassVar[ClientPool]

  def __init__(self) -> None:
    raise NotImplementedError

  @classmethod
  def initiate(cls, workers: int = 1) -> None:
    cls.pool = ClientPool(mc=Client([MEMCACHED_HOST]), n_slots=MEMCACHED_POOL_SIZE // workers)


class Postgres:
  pool: ClassVar[Pool]

  def __init__(self) -> None:
    raise NotImplementedError

  @classmethod
  async def initiate(cls, workers: int = 1) -> None:
    cls.pool = await create_pool(
      POSTGRES_URI,
      max_size=POSTGRES_POOL_SIZE // workers,
      max_inactive_connection_lifetime=300,
      min_size=1,
    )

  @classmethod
  async def close(cls) -> None:
    if cls.pool is not None:
      await cls.pool.close()


async def create_device(scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
  body: bytes = b""
  more_body: bool = True
  while more_body:
    message: ASGIReceiveEvent = await receive()
    assert message["type"] == "http.request"
    body += message.get("body", b"")
    more_body = message.get("more_body", False)
  try:
    device: Final[Device] = Device.from_bytes(body)
    now: Final[datetime] = datetime.now(timezone.utc)
    device_uuid: Final[UUID] = uuid()
    start_time_pg: Final[float] = perf_counter()
    async with Postgres.pool.acquire() as connection:
      firmware: Final[str] = device.firmware
      mac: Final[str] = device.mac
      insert_query: Final[str] = f"""
        INSERT INTO spartan_device (uuid, mac, firmware, created_at, updated_at)
        VALUES ('{device_uuid}', '{mac}', '{firmware}', '{now}', '{now}')
        RETURNING id;
      """
      row: Record = await connection.fetchrow(insert_query)
    end_time_pg: Final[float] = perf_counter()
    duration_pg: Final[float] = end_time_pg - start_time_pg
    H_POSTGRES_LABEL.observe(duration_pg)
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
    device_dict: Final[dict[str, str]] = {
      "id": row["id"],
      "uuid": str(device_uuid),
      "mac": device.mac,
      "firmware": device.firmware,
      "created_at": now.isoformat(),
      "updated_at": now.isoformat(),
    }
    start_time_mc: Final[float] = perf_counter()
    with Memcached.pool.reserve() as client:
      client.set(
        device_uuid.hex.encode(),
        encode(device_dict).decode("utf-8"),
        time=20,
      )
    end_time_mc: Final[float] = perf_counter()
    duration_mc: Final[float] = end_time_mc - start_time_mc
    H_MEMCACHED_LABEL.observe(duration_mc)
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
        "body": encode(device_dict),
      }
    )
  except PostgresError:
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
  except TypeError:
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
  except (SocketError, ValueError):
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


async def get_devices(scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
  """Get static list of devices"""
  devices: Final[tuple[dict[str, int | str], ...]] = (
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
      "body": encode(devices),
    }
  )


async def get_device_stats(
  scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable
) -> None:
  try:
    stats: list[tuple[bytes, dict[bytes, Any]]]
    stats_data: Final[dict[str, str]] = {}
    with Memcached.pool.reserve() as client:
      stats = client.get_stats()
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
        "body": encode(stats_data),
      }
    )
  except (SocketError, ValueError):
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
  except Exception:
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


async def lifespan(receive: ASGIReceiveCallable, send: ASGISendCallable, workers: int) -> None:
  while 1:
    message: ASGIReceiveEvent = await receive()
    if message["type"] == "lifespan.shutdown":
      try:
        await Postgres.close()
        await send({"type": "lifespan.shutdown.complete"})
      except Exception:
        await send({"type": "lifespan.shutdown.failed"})
      break
    elif message["type"] == "lifespan.startup":
      try:
        Memcached.initiate(workers=workers)
        await Postgres.initiate(workers=workers)
        await send({"type": "lifespan.startup.complete"})
      except Exception:
        await send({"type": "lifespan.startup.failed"})


__all__: Final[tuple[str, ...]] = (
  "Memcached",
  "Postgres",
  "create_device",
  "get_devices",
  "get_device_stats",
  "health",
  "lifespan",
)
