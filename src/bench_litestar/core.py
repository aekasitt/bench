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

### Third-party packages ###
from litestar import Litestar
from litestar.handlers.http_handlers import HTTPRouteHandler
from litestar.status_codes import HTTP_201_CREATED

### Local modules ###
from bench_litestar.routes import create_device, get_device_stats, get_devices, health, metrics

health_handler = HTTPRouteHandler("/healthz", http_method="GET", sync_to_thread=True)(health)
metrics_handler = HTTPRouteHandler("/metrics", http_method="GET", sync_to_thread=True)(metrics)
devices_handler = HTTPRouteHandler("/api/devices", http_method="GET", sync_to_thread=True)(
  get_devices
)
create_device_handler = HTTPRouteHandler(
  "/api/devices", http_method="POST", status_code=HTTP_201_CREATED
)(create_device)
device_stats_handler = HTTPRouteHandler("/api/devices/stats", http_method="GET")(get_device_stats)

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
  from uvicorn import run

  run("bench_litestar.core:app", port=8080, workers=16)


if __name__ == "__main__":
  main()


__all__ = ("app", "main")
