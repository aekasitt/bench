#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/litestr/core.py
# VERSION:     0.1.0
# CREATED:     2025-06-24 02:38
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from litestar import Litestar, get, post
from litestar.status_codes import HTTP_201_CREATED

### Local modules ###
from bench.litestr.routes import create_device, get_device_stats, get_devices, health, metrics

health_handler = get("/healthz", sync_to_thread=True)(health)
metrics_handler = get("/metrics", sync_to_thread=True)(metrics)
devices_handler = get("/api/devices", sync_to_thread=True)(get_devices)
create_device_handler = post("/api/devices", status_code=HTTP_201_CREATED)(create_device)
device_stats_handler = get("/api/devices/stats")(get_device_stats)

app = Litestar(
  route_handlers=[
    health_handler,
    metrics_handler,
    devices_handler,
    create_device_handler,
    device_stats_handler,
  ],
)


def main() -> None:
  from psutil import cpu_count
  from uvicorn import run

  # NOTE: https://sentry.io/answers/number-of-uvicorn-workers-needed-in-production/
  physical_cores: int = cpu_count(logical=False)
  logical_cores: int = cpu_count(logical=True)
  threads_per_core: int = logical_cores // physical_cores
  workers: int = physical_cores * threads_per_core + 1

  run("bench.litestr.core:app", log_level="error", port=8080, workers=workers)


if __name__ == "__main__":
  main()


__all__: tuple[str, ...] = ("app", "main")
