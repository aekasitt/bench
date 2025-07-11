#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/litestr/cache.py
# VERSION:     0.1.0
# CREATED:     2025-06-24 02:38
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from logging import Logger, getLogger

### Third-party packages ###
from aiomcache import Client
from aiomcache.exceptions import ClientException
from litestar.exceptions import HTTPException

### Local modules ###
from bench.litestr.configs import MEMCACHED_HOST, MEMCACHED_POOL_SIZE

### Initiate module logger ###
logger: Logger = getLogger(__name__)


def get_memcached() -> Client:
  """Get Memcached client instance"""
  try:
    client = Client(host=MEMCACHED_HOST, pool_size=MEMCACHED_POOL_SIZE)
    logger.info("Memcached pool created successfully")
    return client
  except ClientException as e:
    raise HTTPException(status_code=503, detail=f"Memcached error: {e}")


__all__: tuple[str, ...] = ("get_memcached",)
