#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/starlette/applications.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Callable, List, Optional

### Local modules ###
from .routing import Route


class Starlette:
    """Starlette ASGI application"""
    
    def __init__(
        self,
        routes: Optional[List[Route]] = None,
        **kwargs: Any
    ) -> None:
        """
        Initialize Starlette application
        
        Args:
            routes: List of route handlers
            **kwargs: Additional keyword arguments
        """
        ...
    
    def add_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        methods: Optional[List[str]] = None,
        **kwargs: Any
    ) -> None:
        """
        Add a route to the application
        
        Args:
            path: The URL path for the route
            endpoint: The function to handle the request
            methods: List of HTTP methods to accept
            **kwargs: Additional keyword arguments
        """
        ...


__all__: tuple[str, ...] = ("Starlette",) 