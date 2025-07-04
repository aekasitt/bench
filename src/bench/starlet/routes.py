#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/starlet/routes.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
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
from typing import Any
from uuid import uuid4 as uuid

### Third-party packages ###
from asyncpg.exceptions import PostgresError
from orjson import dumps
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR

### Local modules ###
from bench.starlet.cache import get_memcached
from bench.starlet.database import get_postgres_connection
from bench.starlet.metrics import H

### Initiate module logger ###
logger: Logger = getLogger(__name__)


class DeviceRequest:
  def __init__(self, mac: str, firmware: str) -> None:
    self.mac = mac
    self.firmware = firmware


H_MEMCACHED_LABEL = H.labels(op="set", db="memcache")
H_POSTGRES_LABEL = H.labels(op="insert", db="postgres")


async def health(request: Request) -> PlainTextResponse:
  """Health check endpoint"""
  return PlainTextResponse("OK")


async def metrics(request: Request) -> Response:
  """Prometheus metrics endpoint"""
  return Response(
    content=generate_latest(),
    media_type=CONTENT_TYPE_LATEST,
  )


async def get_devices(request: Request) -> JSONResponse:
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

  return JSONResponse(devices)


async def create_device(request: Request) -> JSONResponse:
  """Create a new device"""
  try:
    # Parse request body
    body: Any = await request.json()
    device = DeviceRequest(mac=body["mac"], firmware=body["firmware"])

    now = datetime.now(timezone.utc)
    device_uuid = uuid()

    insert_query = """
            INSERT INTO starlette_device (uuid, mac, firmware, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id;
            """

    start_time: float = perf_counter()

    postgres = await get_postgres_connection()
    row = await postgres.fetchrow(insert_query, device_uuid, device.mac, device.firmware, now, now)

    H_POSTGRES_LABEL.observe(perf_counter() - start_time)

    if not row:
      return JSONResponse(
        {"detail": "Failed to create device record"}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
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

    memcached = get_memcached()
    await memcached.set(
      device_uuid.hex.encode(),
      dumps(device_dict),
      exptime=20,
    )

    H_MEMCACHED_LABEL.observe(perf_counter() - start_time)

    return JSONResponse(device_dict, status_code=HTTP_201_CREATED)

  except PostgresError:
    logger.exception("Postgres error")
    return JSONResponse(
      {"detail": "Database error occurred while creating device"},
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

  except (SocketError, ValueError):
    logger.exception("Memcached error")
    return JSONResponse(
      {"detail": "Memcached Database error occurred while creating device"},
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

  except Exception:
    logger.exception("Unknown error")
    return JSONResponse(
      {"detail": "An unexpected error occurred while creating device"},
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def get_device_stats(request: Request) -> JSONResponse:
  """Get memcached statistics"""
  try:
    memcached = get_memcached()
    stats = memcached.get_stats()
    _, result = stats[0]
    return JSONResponse(
      {
        "curr_items": result.get(b"curr_items", 0),
        "total_items": result.get(b"total_items", 0),
        "bytes": result.get(b"bytes", 0),
        "curr_connections": result.get(b"curr_connections", 0),
        "get_hits": result.get(b"get_hits", 0),
        "get_misses": result.get(b"get_misses", 0),
      }
    )
  except (SocketError, ValueError):
    logger.exception("Memcached error")
    return JSONResponse(
      {"detail": "Memcached error occurred while retrieving stats"},
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )
  except Exception:
    logger.exception("Unknown error")
    return JSONResponse(
      {"detail": "An unexpected error occurred while retrieving stats"},
      status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


__all__: tuple[str, ...] = ("health", "metrics", "get_devices", "create_device", "get_device_stats")
