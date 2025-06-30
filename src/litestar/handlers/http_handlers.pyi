#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/litestar/handlers/http_handlers.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-30 12:22
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Callable, TypeVar


F = TypeVar("F", bound=Callable[..., Any])


def HTTPRouteHandler(
    path: str,
    *,
    http_method: str,
    sync_to_thread: bool = False,
    status_code: None | int = None,
    **kwargs: Any
) -> Callable[[F], F]:
    """
    HTTP Route Handler decorator for Litestar framework

    Args:
        path: The URL path for the route
        http_method: The HTTP method (GET, POST, etc.)
        sync_to_thread: Whether to run the handler in a thread pool
        status_code: The status code to return
        **kwargs: Additional keyword arguments

    Returns:
        A decorator function that can be applied to handler functions
    """
    ...


__all__: tuple[str, ...] = ("HTTPRouteHandler",)
