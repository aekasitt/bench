#!/usr/bin/env python3.13
"""
Type stubs for orjson package.
"""

### Standard packages ###
from typing import Any, Dict, List, Optional, Union

### Type aliases ###
JSONValue = Union[
    None,
    bool,
    int,
    float,
    str,
    List[Any],
    Dict[str, Any]
]

### Functions ###
def dumps(
    obj: Any,
    *,
    default: Optional[Any] = None,
    option: Optional[int] = None,
) -> bytes: ...

def loads(
    obj: Union[bytes, bytearray, memoryview, str],
    *,
    option: Optional[int] = None,
) -> JSONValue: ...

### Constants ###
# Serialization options
OPT_INDENT_2: int = ...
OPT_NAIVE_UTC: int = ...
OPT_NON_STR_KEYS: int = ...
OPT_OMIT_MICROSECONDS: int = ...
OPT_PASSTHROUGH_DATETIME: int = ...
OPT_PASSTHROUGH_SUBCLASS: int = ...
OPT_SERIALIZE_DATETIME: int = ...
OPT_SERIALIZE_NUMPY: int = ...
OPT_SERIALIZE_UUID: int = ...
OPT_STRICT_INTEGER: int = ...
OPT_UNICODE_ESCAPE: int = ...

# Error types
JSONDecodeError: type[Exception] = ...
JSONEncodeError: type[Exception] = ...

__all__: tuple[str, ...] = (
    "dumps",
    "loads",
    "OPT_INDENT_2",
    "OPT_NAIVE_UTC",
    "OPT_NON_STR_KEYS",
    "OPT_OMIT_MICROSECONDS",
    "OPT_PASSTHROUGH_DATETIME",
    "OPT_PASSTHROUGH_SUBCLASS",
    "OPT_SERIALIZE_DATETIME",
    "OPT_SERIALIZE_NUMPY",
    "OPT_SERIALIZE_UUID",
    "OPT_STRICT_INTEGER",
    "OPT_UNICODE_ESCAPE",
    "JSONDecodeError",
    "JSONEncodeError",
) 