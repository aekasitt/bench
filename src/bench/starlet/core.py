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

### Third-party packages ###
from starlette.applications import Starlette
from starlette.routing import Route

### Local modules ###
from bench.starlet.routes import create_device, get_device_stats, get_devices, health, metrics

# Create routes
routes = [
  Route("/healthz", endpoint=health, methods=["GET"]),
  Route("/metrics", endpoint=metrics, methods=["GET"]),
  Route("/api/devices", endpoint=get_devices, methods=["GET"]),
  Route("/api/devices", endpoint=create_device, methods=["POST"]),
  Route("/api/devices/stats", endpoint=get_device_stats, methods=["GET"]),
]

# Create Starlette application
app = Starlette(routes=routes)


def main() -> None:
  from psutil import cpu_count
  from uvicorn import run

  # NOTE: https://sentry.io/answers/number-of-uvicorn-workers-needed-in-production/
  physical_cores: int = cpu_count(logical=False)
  logical_cores: int = cpu_count(logical=True)
  threads_per_core: int = logical_cores // physical_cores
  workers: int = physical_cores * threads_per_core + 1

  run("bench.starlet.core:app", log_level="error", port=8080, workers=workers)


if __name__ == "__main__":
  main()


__all__: tuple[str, ...] = ("app", "main")
