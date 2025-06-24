#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_fastapi/core.py
# VERSION:     0.1.0
# CREATED:     2025-01-22 15:23
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
from aiomcache.exceptions import ClientException
from asyncpg import PostgresError
from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse, PlainTextResponse
from orjson import dumps
from prometheus_client import make_asgi_app
from pydantic import BaseModel

### Local modules ###
from bench_fastapi.cache import Memcached
from bench_fastapi.database import Postgres
from bench_fastapi.metrics import H

### Initiate module logger ###
logger: Logger = getLogger(__name__)

app = FastAPI()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/healthz", response_class=PlainTextResponse)
def health():
  return "OK"


@app.get("/api/devices", response_class=ORJSONResponse)
def get_devices():
  devices = (
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


class DeviceRequest(BaseModel):
  mac: str
  firmware: str


H_MEMCACHED_LABEL = H.labels(op="set", db="memcache")
H_POSTGRES_LABEL = H.labels(op="insert", db="postgres")


@app.post("/api/devices", status_code=201, response_class=ORJSONResponse)
async def create_device(device: DeviceRequest, postgres: Postgres, memcached: Memcached):
  try:
    now = datetime.now(timezone.utc)
    device_uuid = uuid()

    insert_query = """
            INSERT INTO fastapi_device (uuid, mac, firmware, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id;
            """

    start_time: float = perf_counter()

    row = await postgres.fetchrow(insert_query, device_uuid, device.mac, device.firmware, now, now)

    H_POSTGRES_LABEL.observe(perf_counter() - start_time)

    if not row:
      raise HTTPException(status_code=500, detail="Failed to create device record")

    device_dict = {
      "id": row["id"],
      "uuid": str(device_uuid),
      "mac": device.mac,
      "firmware": device.firmware,
      "created_at": now,  #
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
    raise HTTPException(status_code=500, detail="Database error occurred while creating device")

  except (ClientException, SocketError):
    logger.exception("Memcached error")
    raise HTTPException(
      status_code=500,
      detail=" Memcached Database error occurred while creating device",
    )

  except Exception as err:
    logger.exception("Unknown error")
    raise HTTPException(
      status_code=500, detail="An unexpected error occurred while creating device"
    )


@app.get("/api/devices/stats", response_class=ORJSONResponse)
async def get_device_stats(memcached: Memcached):
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
    raise HTTPException(status_code=500, detail="Memcached error occurred while retrieving stats")
  except Exception as err:
    logger.exception("Unknown error")
    raise HTTPException(
      status_code=500,
      detail="An unexpected error occurred while retrieving stats",
    )


def main() -> None:
  from uvicorn import run

  run("bench_fastapi.core:app", port=8080, workers=10)


if __name__ == "__main__":
  main()

__all__ = ("app", "main")
