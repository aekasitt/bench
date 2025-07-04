#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/starlette/routing.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Callable, List, Optional

class Route:
  """Starlette route handler"""

  def __init__(
    self,
    path: str,
    endpoint: Callable[..., Any],
    methods: Optional[List[str]] = None,
    **kwargs: Any,
  ) -> None:
    """
    Initialize route

    Args:
        path: The URL path for the route
        endpoint: The function to handle the request
        methods: List of HTTP methods to accept
        **kwargs: Additional keyword arguments
    """
    ...

  @property
  def path(self) -> str:
    """Get the route path"""
    ...

  @property
  def endpoint(self) -> Callable[..., Any]:
    """Get the endpoint function"""
    ...

  @property
  def methods(self) -> List[str]:
    """Get the allowed HTTP methods"""
    ...

__all__: tuple[str, ...] = ("Route",)
