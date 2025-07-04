#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/starlet/cache.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from logging import Logger, getLogger
from typing import Final

### Third-party packages ###
from pylibmc.client import Client
from starlette.exceptions import HTTPException

### Local modules ###
from bench.starlet.configs import MEMCACHED_HOST

### Initiate module logger ###
logger: Logger = getLogger(__name__)


def get_memcached() -> Client:
  """Get Memcached client instance"""
  try:
    client = Client([MEMCACHED_HOST])
    logger.info("Memcached pool created successfully")
    return client
  except ValueError as e:
    raise HTTPException(status_code=503, detail=f"Memcached error: {e}")


__all__: Final[tuple[str, ...]] = ("get_memcached",)
