#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/starlette/requests.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Dict, Optional


class Request:
    """Starlette request object"""
    
    def __init__(self, scope: Dict[str, Any], receive: Any, send: Any) -> None:
        """
        Initialize request object
        
        Args:
            scope: ASGI scope dictionary
            receive: ASGI receive callable
            send: ASGI send callable
        """
        ...
    
    async def json(self) -> Any:
        """
        Parse request body as JSON
        
        Returns:
            Parsed JSON data
        """
        ...
    
    @property
    def method(self) -> str:
        """Get the HTTP method"""
        ...
    
    @property
    def url(self) -> str:
        """Get the request URL"""
        ...
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get the request headers"""
        ...
    
    @property
    def query_params(self) -> Dict[str, str]:
        """Get the query parameters"""
        ...


__all__: tuple[str, ...] = ("Request",) 