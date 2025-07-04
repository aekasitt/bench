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
from typing import Final, Type

### Third-party packages ###
from pylibmc.client import Client

### Local modules ###
from bench_uvicorn.configs import MEMCACHED_HOST


class Memcached:
  """Get Memcached client instance"""

  client: Client

  def __enter__(self) -> "Memcached":
    self.client = Client([MEMCACHED_HOST])
    return self

  def __exit__(
    self, exc_type: None | Type[BaseException], exc: Type[BaseException], tb: TracebackType
  ) -> None:
    self.client.disconnect_all()


__all__: Final[tuple[str, ...]] = ("Memcached",)
