#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/starlet/core.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from contextlib import asynccontextmanager
from typing import AsyncGenerator

### Third-party packages ###
from psutil import cpu_count
from starlette.applications import Starlette
from starlette.routing import Route

### Local modules ###
from bench.starlet.cache import MemcachedPool
from bench.starlet.database import PostgresPool
from bench.starlet.routes import create_device, get_device_stats, get_devices, health, metrics


# NOTE: https://sentry.io/answers/number-of-uvicorn-workers-needed-in-production/
physical_cores: int = cpu_count(logical=False) or 1
logical_cores: int = cpu_count(logical=True) or 1
threads_per_core: int = logical_cores // physical_cores
workers: int = physical_cores * threads_per_core + 1


@asynccontextmanager
async def lifespan(app: Starlette) -> AsyncGenerator[None, None]:
  MemcachedPool.initiate(workers=workers)
  await PostgresPool.initiate(workers=workers)
  yield
  MemcachedPool.close()
  await PostgresPool.close()


routes = [
  Route("/healthz", endpoint=health, methods=["GET"]),
  Route("/metrics", endpoint=metrics, methods=["GET"]),
  Route("/api/devices", endpoint=get_devices, methods=["GET"]),
  Route("/api/devices", endpoint=create_device, methods=["POST"]),
  Route("/api/devices/stats", endpoint=get_device_stats, methods=["GET"]),
]
app = Starlette(lifespan=lifespan, routes=routes)


def main() -> None:
  from uvicorn import run

  run("bench.starlet.core:app", log_level="error", port=8080, workers=workers)


if __name__ == "__main__":
  main()


__all__: tuple[str, ...] = ("app", "main")
