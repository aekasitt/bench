#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_litestar/core.py
# VERSION:     0.1.0
# CREATED:     2025-06-24 02:38
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from datetime import datetime, timezone
from logging import Logger, getLogger
from socket import gaierror as SocketError
from time import perf_counter
from uuid import uuid4 as uuid

### Third-party packages ###
from aiomcache import Client
from aiomcache.exceptions import ClientException
from asyncpg import Connection, Record
from asyncpg.exceptions import PostgresError
from litestar import Litestar, get, post
from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.response import Response
from litestar.status_codes import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from msgspec import Struct
from orjson import dumps
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

### Local modules ###
from bench_litestar.cache import get_memcached
from bench_litestar.database import get_postgres_connection
from bench_litestar.metrics import H

### Initiate module logger ###
logger: Logger = getLogger(__name__)


class DeviceRequest(Struct):
  mac: str
  firmware: str


H_MEMCACHED_LABEL = H.labels(op="set", db="memcache")
H_POSTGRES_LABEL = H.labels(op="insert", db="postgres")


@get("/healthz", sync_to_thread=False)
def health() -> str:
  return "OK"


@get("/metrics", sync_to_thread=False)
def metrics() -> Response[bytes]:
  """Prometheus metrics endpoint"""
  return Response(
    content=generate_latest(),
    media_type=CONTENT_TYPE_LATEST,
  )


@get("/api/devices", sync_to_thread=False)
def get_devices() -> tuple[dict[str, int | str], ...]:
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

  return devices


@post("/api/devices", status_code=HTTP_201_CREATED)
async def create_device(
  device: DeviceRequest,
  postgres: Connection,
  memcached: Client,
) -> dict[str, datetime | str]:
  try:
    now = datetime.now(timezone.utc)
    device_uuid = uuid()

    insert_query = """
            INSERT INTO litestar_device (uuid, mac, firmware, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id;
            """

    start_time: float = perf_counter()

    row: Record | None = await postgres.fetchrow(insert_query, device_uuid, device.mac, device.firmware, now, now)

    H_POSTGRES_LABEL.observe(perf_counter() - start_time)

    if not row:
      raise HTTPException(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create device record"
      )

    device_dict = {
      "id": row["id"],
      "uuid": str(device_uuid),
      "mac": device.mac,
      "firmware": device.firmware,
      "created_at": now,
      "updated_at": now,
    }

    # Measure cache operation
    start_time = perf_counter()

    await memcached.set(
      device_uuid.hex.encode(),
      dumps(device_dict),
      exptime=20,
    )

    H_MEMCACHED_LABEL.observe(perf_counter() - start_time)

    return device_dict

  except PostgresError:
    logger.exception("Postgres error")
    raise HTTPException(
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Database error occurred while creating device",
    )

  except (ClientException, SocketError):
    logger.exception("Memcached error")
    raise HTTPException(
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Memcached Database error occurred while creating device",
    )

  except Exception:
    logger.exception("Unknown error")
    raise HTTPException(
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
      detail="An unexpected error occurred while creating device",
    )


@get("/api/devices/stats")
async def get_device_stats(memcached: Client) -> dict[str, None | bytes | int | str]:
  try:
    stats = await memcached.stats()
    return {
      "curr_items": stats.get(b"curr_items", 0),
      "total_items": stats.get(b"total_items", 0),
      "bytes": stats.get(b"bytes", 0),
      "curr_connections": stats.get(b"curr_connections", 0),
      "get_hits": stats.get(b"get_hits", 0),
      "get_misses": stats.get(b"get_misses", 0),
    }
  except (ClientException, SocketError):
    logger.exception("Memcached error")
    raise HTTPException(
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Memcached error occurred while retrieving stats",
    )
  except Exception:
    logger.exception("Unknown error")
    raise HTTPException(
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
      detail="An unexpected error occurred while retrieving stats",
    )


app = Litestar(
  route_handlers=[
    health,
    metrics,
    get_devices,
    create_device,
    get_device_stats,
  ],
  dependencies={
    "postgres": Provide(get_postgres_connection),
    "memcached": Provide(get_memcached),
  },
)


def main() -> None:
  from uvicorn import run

  run("bench_litestar.core:app", port=8080, workers=4)


if __name__ == "__main__":
  main()


__all__ = ("app", "main")
