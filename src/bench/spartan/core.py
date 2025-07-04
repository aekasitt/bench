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

### Third-party packages ###
from uvicorn._types import HTTPScope, ASGIReceiveCallable, ASGISendCallable

### Local modules ###
from bench.spartan.routes import create_device, get_devices, get_device_stats, health


async def app(scope: HTTPScope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
  assert scope["type"] == "http"
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
  from psutil import cpu_count
  from uvicorn import run

  # NOTE: https://sentry.io/answers/number-of-uvicorn-workers-needed-in-production/
  physical_cores: int = cpu_count(logical=False)
  logical_cores: int = cpu_count(logical=True)
  threads_per_core: int = logical_cores // physical_cores
  workers: int = physical_cores * threads_per_core + 1

  run("bench.spartan.core:app", log_level="error", port=8080, workers=workers)


if __name__ == "__main__":
  main()


__all__: tuple[str, ...] = ("app", "main")
