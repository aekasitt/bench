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
from json import dumps
from logging import Logger, getLogger
from socket import gaierror as SocketError
from typing import Any

### Third-party packages ###
from aiomcache.exceptions import ClientException
# from uvicorn._types import HTTPScope, ASGIReceiveCallable, ASGISendCallable

### Local modules ###
from bench_uvicorn.cache import get_memcached

### Initiate module logger ###
logger: Logger = getLogger("uvicorn")


async def health(
  scope: Any, receive: Any, send: Any
) -> None:
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


async def get_devices(
  scope: Any, receive: Any, send: Any
) -> None:
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
  memcached = get_memcached()
  try:
    stats = await memcached.stats()
    stats_data = {
      "curr_items": stats.get(b"curr_items", b"0").decode("utf-8"),
      "total_items": stats.get(b"total_items", b"0").decode("utf-8"),
      "bytes": stats.get(b"bytes", b"0").decode("utf-8"),
      "curr_connections": stats.get(b"curr_connections", b"0").decode("utf-8"),
      "get_hits": stats.get(b"get_hits", b"0").decode("utf-8"),
      "get_misses": stats.get(b"get_misses", b"0").decode("utf-8"),
    }
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
  except (ClientException, SocketError):
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
        "body": b"Memcached error occurred while retrieving stats",
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
        "body": b"An unexpected error occurred while retrieving stats",
      }
    )


__all__: tuple[str, ...] = ("health", "get_devices")
