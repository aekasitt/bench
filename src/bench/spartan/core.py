#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/spartan/core.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from __future__ import annotations
from typing import Literal

### Third-party packages ###
from gc import set_threshold
from psutil import cpu_count
from uvicorn._types import ASGIReceiveCallable, ASGISendCallable, Scope

### Local modules ###
from bench.spartan.routes import (
  Memcached,
  Postgres,
  create_device,
  get_devices,
  get_device_stats,
  health,
)


# NOTE: https://sentry.io/answers/number-of-uvicorn-workers-needed-in-production/
physical_cores: int = cpu_count(logical=False) or 1
logical_cores: int = cpu_count(logical=True) or 1
threads_per_core: int = logical_cores // physical_cores
workers: int = physical_cores * threads_per_core + 1


# NOTE: https://mypyc.readthedocs.io/en/latest/performance_tips_and_tricks.html#adjusting-garbage-collection
set_threshold(80_000)


async def app(scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
  if scope["type"] == "lifespan":
    while True:
      message: dict[Literal["type"], str] = await receive()
      if message["type"] == "lifespan.startup":
        try:
          Memcached.initiate(workers=workers)
          await Postgres.initiate(workers=workers)
          await send({"type": "lifespan.startup.complete"})
        except Exception:
          await send({"type": "lifespan.startup.failed"})
      elif message["type"] == "lifespan.shutdown":
        try:
          await Postgres.close()
          await send({"type": "lifespan.shutdown.complete"})
        except Exception:
          await send({"type": "lifespan.shutdown.failed"})
        finally:
          return

  path: str = scope["path"]
  method: str = scope["method"]

  if path == "/api/devices" and method == "GET":
    await get_devices(scope, receive, send)
  elif path == "/api/devices" and method == "POST":
    await create_device(scope, receive, send)
  elif path == "/api/devices/stats" and method == "GET":
    await get_device_stats(scope, receive, send)
  elif path == "/healthz" and method == "GET":
    await health(scope, receive, send)


def main() -> None:
  from uvicorn import run

  run("bench.spartan.core:app", log_level="info", port=8080, workers=1)


if __name__ == "__main__":
  main()


__all__: tuple[str, ...] = ("app", "main")
