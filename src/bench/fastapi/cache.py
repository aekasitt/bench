#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/fastapi/cache.py
# VERSION:     0.1.0
# CREATED:     2025-01-22 15:23
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from contextlib import contextmanager
from logging import Logger, getLogger
from typing import Final, Generator

### Third-party packages ###
from pylibmc.client import Client
from pylibmc.pools import ClientPool
from starlette.requests import Request
from starlette.responses import Response

### Local modules ###
from bench.fastapi.configs import MEMCACHED_HOST, MEMCACHED_POOL_SIZE

logger: Logger = getLogger(__name__)


class MemcachedPool:
  pool: ClientPool | None = None

  @classmethod
  def init(cls, workers: int = 1) -> None:
    client: Client = Client(servers=[MEMCACHED_HOST])
    cls.pool = ClientPool(client, n_slots=MEMCACHED_POOL_SIZE // workers)


class Memcached:
  def __call__(self, request: Request, response: Response) -> "Memcached":
    if MemcachedPool.pool is None:
      logger.exception("Please initiate MemcachedPool instance during FastAPI lifespan")
    return self

  @contextmanager
  def reserve(self) -> Generator[Client, None, None]:
    with MemcachedPool.pool.reserve() as client:
      yield client
      client.disconnect_all()


__all__: Final[tuple[str, ...]] = ("Memcached", "MemcachedPool")
