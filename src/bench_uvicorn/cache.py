#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_starlette/cache.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from types import TracebackType
from typing import Type

### Third-party packages ###
from pymemcache.client.base import Client

### Local modules ###
from bench_litestar.configs import MEMCACHED_HOST, MEMCACHED_POOL_SIZE


class Memcached:
  """Get Memcached client instance"""

  client: Client

  def __enter__(self) -> "Memcached":
    self.client = Client(f"{MEMCACHED_HOST}:11211")  #, max_pool_size=MEMCACHED_POOL_SIZE)
    return self

  def __exit__(
    self,
    exc_type: None | Type[BaseException],
    exc: Type[BaseException],
    tb: TracebackType
  ) -> None:
    self.client.close()


__all__: tuple[str, ...] = ("Memcached",)
