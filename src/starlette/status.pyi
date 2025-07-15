#!/usr/bin/env python3.13
"""
Type stubs for starlette status codes
"""

### Standard packages ###
from typing import Final

HTTP_200_OK: int = 200
HTTP_201_CREATED: int = 201
HTTP_500_INTERNAL_SERVER_ERROR: int = 500


__all__: Final[tuple[str, ...]] = (
  "HTTP_200_OK",
  "HTTP_201_CREATED",
  "HTTP_500_INTERNAL_SERVER_ERROR",
)
