"""
Type stubs for aiomcache exceptions module.
"""

class ClientException(Exception):
  """Base exception for aiomcache client errors."""

  pass

class ValidationException(ClientException):
  """Exception raised for validation errors."""

  pass

class MemcacheError(ClientException):
  """Exception raised for memcache protocol errors."""

  pass
