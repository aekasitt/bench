#!/usr/bin/env python3.13
"""
Type stubs for prometheus_client package.
"""

### Standard packages ###
from typing import Any, Callable

CONTENT_TYPE_LATEST: str

class Histogram:
  def __init__(
    self,
    name: str,
    documentation: str,
    labelnames: None | tuple[str, ...] = None,
    namespace: str = "",
    subsystem: str = "",
    unit: str = "",
    buckets: None | tuple[float, ...] = None,
    **kwargs: Any,
  ) -> None:
    """TODO"""

  def labels(self, **labelvalues: str) -> "Histogram":
    """TODO"""

  def observe(self, amount: float) -> None:
    """TODO"""

  def time(self) -> Callable[[], None]:
    """TODO"""

def generate_latest() -> bytes:
  """TODO"""

__all__: tuple[str, ...] = ("CONTENT_TYPE_LATEST", "Histogram", "generate_latest")
