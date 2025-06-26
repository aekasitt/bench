#!/usr/bin/env python3.13
"""
Type stubs for python-dotenv package.
"""

### Standard packages ###
from typing import Any, Optional, Union


def load_dotenv(
  dotenv_path: Optional[Union[str, bytes]] = None,
  stream: Optional[Union[str, bytes]] = None,
  verbose: bool = False,
  override: bool = False,
  **kwargs: Any,
) -> bool:
  """TODO"""


def find_dotenv(
  filename: str = ".env", raise_error_if_not_found: bool = False, usecwd: bool = False
) -> str:
  """TODO"""


def dotenv_values(
  dotenv_path: None | bytes | str = None,
  stream: None | bytes | str = None,
  verbose: bool = False,
  **kwargs: Any,
) -> dict[str, None | str]:
  """TODO"""


__all__: tuple[str, ...] = ("load_dotenv", "find_dotenv", "dotenv_values")
