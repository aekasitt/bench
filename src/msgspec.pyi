#!/usr/bin/env python3.13
"""
Type stubs for msgspec package.
"""

### Standard packages ###
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

### Type variables ###
T = TypeVar("T")

### Classes ###
class Struct:
    """Base class for structured data types."""
    
    def __init__(self, **kwargs: Any) -> None: ...
    
    def __repr__(self) -> str: ...
    
    def __eq__(self, other: Any) -> bool: ...
    
    def __hash__(self) -> int: ...

class Raw(Generic[T]):
    """Raw message type for msgspec."""
    
    def __init__(self, value: T) -> None: ...
    
    @property
    def value(self) -> T: ...

### Functions ###
def encode(
    obj: Any,
    *,
    enc_hook: Optional[Any] = None,
    **kwargs: Any
) -> bytes: ...

def decode(
    obj: Union[bytes, bytearray],
    *,
    type: Optional[Any] = None,
    dec_hook: Optional[Any] = None,
    **kwargs: Any
) -> Any: ...

def to_builtins(
    obj: Any,
    *,
    enc_hook: Optional[Any] = None,
    **kwargs: Any
) -> Any: ...

def from_builtins(
    obj: Any,
    *,
    type: Optional[Any] = None,
    dec_hook: Optional[Any] = None,
    **kwargs: Any
) -> Any: ...

### Decorators ###
def field(
    *,
    default: Any = ...,
    default_factory: Optional[Any] = None,
    name: Optional[str] = None,
    **kwargs: Any
) -> Any: ...

### Constants ###
UNSET: Any = ...

__all__: tuple[str, ...] = (
    "Struct",
    "Raw", 
    "encode",
    "decode",
    "to_builtins",
    "from_builtins",
    "field",
    "UNSET",
) 