#!/usr/bin/env python3.12
"""
Type stubs for starlette exceptions
"""

class HTTPException(Exception):
  """Exception thrown by HTTP endpoint"""

  def __init__(self, status_code: int, detail: str) -> None:
    """HTTPException constructor"""

__all__: tuple[str, ...] = ("HTTPException",)
