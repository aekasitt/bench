#!/usr/bin/env python3.13
# Copyright (C) 2025 All rights reserved.
# FILENAME:    ~~/src/starlette/responses.pyi
# VERSION:     0.1.0
# CREATED:     2025-06-30 14:01
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, Dict, Optional

class Response:
  """Base response class"""

  def __init__(
    self,
    content: Any,
    status_code: int = 200,
    headers: Optional[Dict[str, str]] = None,
    media_type: Optional[str] = None,
    **kwargs: Any,
  ) -> None:
    """
    Initialize response

    Args:
        content: Response content
        status_code: HTTP status code
        headers: Response headers
        media_type: Content type
        **kwargs: Additional keyword arguments
    """
    ...

class JSONResponse(Response):
  """JSON response class"""

  def __init__(
    self,
    content: Any,
    status_code: int = 200,
    headers: Optional[Dict[str, str]] = None,
    **kwargs: Any,
  ) -> None:
    """
    Initialize JSON response

    Args:
        content: JSON-serializable content
        status_code: HTTP status code
        headers: Response headers
        **kwargs: Additional keyword arguments
    """
    ...

class PlainTextResponse(Response):
  """Plain text response class"""

  def __init__(
    self,
    content: str,
    status_code: int = 200,
    headers: Optional[Dict[str, str]] = None,
    **kwargs: Any,
  ) -> None:
    """
    Initialize plain text response

    Args:
        content: Text content
        status_code: HTTP status code
        headers: Response headers
        **kwargs: Additional keyword arguments
    """
    ...

__all__: tuple[str, ...] = ("Response", "JSONResponse", "PlainTextResponse")
