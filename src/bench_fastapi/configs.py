#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/bench_fastapi/configs.py
# VERSION:     0.1.0
# CREATED:     2025-01-22 15:23
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from os import getenv

### If development environment, load dotenv ###
try:
  from dotenv import load_dotenv

  load_dotenv(".env")
except ImportError:
  pass

MEMCACHED_HOST: str = getenv("MEMCACHED_HOST", "0.0.0.0")
MEMCACHED_POOL_SIZE: int = int(getenv("MEMCACHED_POOL_SIZE", "500"))
POSTGRES_POOL_SIZE: int = int(getenv("POSTGRES_POOL_SIZE", "20"))
POSTGRES_URI: str = getenv("POSTGRES_URI", "postgres://bench:benchpwd@localhost:5432/benchdb")

__all__ = ("MEMCACHED_HOST", "MEMCACHED_POOL_SIZE", "POSTGRES_POOL_SIZE", "POSTGRES_URI")
