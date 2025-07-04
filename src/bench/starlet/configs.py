#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench/starlet/configs.py
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from os import getenv
from typing import Final

### If development environment, load dotenv ###
try:
  from dotenv import load_dotenv

  load_dotenv(".env")
except ImportError:
  pass

MEMCACHED_HOST: Final[str] = getenv("MEMCACHED_HOST", "0.0.0.0")
MEMCACHED_POOL_SIZE: Final[int] = int(getenv("MEMCACHED_POOL_SIZE", "500"))
POSTGRES_POOL_SIZE: Final[int] = int(getenv("POSTGRES_POOL_SIZE", "20"))
POSTGRES_URI: Final[str] = getenv("POSTGRES_URI", "postgres://bench:benchpwd@localhost:5432/benchdb")


__all__: Final[tuple[str, ...]] = (
  "MEMCACHED_HOST",
  "MEMCACHED_POOL_SIZE",
  "POSTGRES_POOL_SIZE",
  "POSTGRES_URI",
)
