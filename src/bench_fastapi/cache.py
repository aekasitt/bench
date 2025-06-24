#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_fastapi/cache.py
# VERSION:     0.1.0
# CREATED:     2025-01-22 15:23
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from logging import Logger, getLogger
from typing import Annotated, AsyncGenerator

### Third-party packages ###
from aiomcache import Client
from aiomcache.exceptions import ClientException
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends

### Local modules ###
from bench_fastapi.configs import MEMCACHED_HOST, MEMCACHED_POOL_SIZE

### Initiate module logger ###
logger: Logger = getLogger(__name__)


async def get_memcached() -> AsyncGenerator[Client, None]:
  """Dependency for getting Memcached client"""
  client: Client | None = None
  try:
    client = Client(host=MEMCACHED_HOST, pool_size=MEMCACHED_POOL_SIZE)
    logger.info("Memcached pool created successfully")
    yield client
  except ClientException as e:
    raise HTTPException(status_code=503, detail=f"Memcached error: {e}")
  finally:
    if client is not None:
      await client.close()


Memcached = Annotated[Client, Depends(get_memcached)]

__all__ = ("Memcached", "get_memcached")
