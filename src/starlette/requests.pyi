#!/usr/bin/env python3.13
"""
Type stubs for starlette Request
"""

### Standard packages ###
from typing import Any, Final


class Request:
  def json(self) -> Any:
    ...


__all__: Final[tuple[str, ...]] = ("Request",)
