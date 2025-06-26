#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_litestar/schema.py
# VERSION:     0.1.0
# CREATED:     2025-06-26 15:16
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from msgspec import Struct


class DeviceRequest(Struct):
    mac: str
    firmware: str


__all__: tuple[str, ...] = ("DeviceRequest",)