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
from contextlib import contextmanager
from logging import Logger, getLogger
from queue import Empty
from typing import ClassVar, Final, Generator

### Third-party packages ###
from pylibmc.client import Client
from pylibmc.pools import ClientPool

### Local modules ###
from bench.starlet.configs import MEMCACHED_HOST, MEMCACHED_POOL_SIZE

logger: Logger = getLogger(__name__)


class MemcachedPool:
  pool: ClassVar[ClientPool]

  @classmethod
  def initiate(cls, workers: int = 1) -> None:
    client: Client = Client(servers=[MEMCACHED_HOST])
    cls.pool = ClientPool(client, n_slots=MEMCACHED_POOL_SIZE // workers)

  @classmethod
  def close(cls) -> None:
    while not cls.pool.empty():
      try:
        cls.pool.get_nowait()
      except Empty:
        break


class Memcached:
  def __init__(self) -> None:
    if MemcachedPool.pool is None:
     logger.exception("Please initiate MemcachedPool instance during FastAPI lifespan")

  @contextmanager
  def reserve(self) -> Generator[Client, None, None]:
    with MemcachedPool.pool.reserve() as client:
      yield client
      client.disconnect_all()


__all__: Final[tuple[str, ...]] = ("Memcached", "MemcachedPool")
